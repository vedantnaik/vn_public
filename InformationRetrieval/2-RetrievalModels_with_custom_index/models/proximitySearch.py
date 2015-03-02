from Tools.Scripts.treesync import raw_input

__author__ = 'Vedant'


def andMapDict(boolDict):
    b = True
    for x in boolDict.values():
        b = b and x
    return b

def minDiff(intArr):
    copyArr=intArr
    if(len(copyArr)==1):
        return 1
    minD = copyArr[1]-copyArr[0]
    copyArr.sort()
    for i in range(2,len(copyArr)):
        minD = min(minD, copyArr[i]-copyArr[i-1])
    if minD<0:
        return -minD
    else:
        return minD

def getSmallestTermInWindow(window):
    minT = float("inf")
    minTerm = ""
    for term in window.keys():
        if window[term] < minT:
            minT = window[term]
            minTerm = term
    return minTerm

def proximitySearch(queryNumber, termFreqDict, avgDocLenOfCorpus, retriever, stemmedArray, vocabSize):
    proximScores = {}
    termPosDict = {}

    for term in stemmedArray:
        dBlock = retriever.getAllDBlocks(term)
        termPosDict.update({term: dBlock})
        # termPosDict   =   {term : dBlock}
        # dBlock        =   {docno: [positions list]}

    for docId in termFreqDict.keys():
        docLen = int(termFreqDict[docId][0])
        blurbDict = {}                      #   blurbDict = {term : [list of positions]}
        window = {}                         #   window = {term : position we are considering}
        termWindowIndexes = {}              #   termWindowIndexes = {term : index of positions in window}
        termsProcessed = {}                 #   termProcessed = {term : True if all the positions are seen}
        for term in termFreqDict[docId][1].keys():
            blurbDict.update({term: termPosDict[term][docId]})
            window.update({term: termPosDict[term][docId][0]})
            termWindowIndexes.update({term: 0})
            termsProcessed.update({term: False})

        smallestRange = minDiff([window[x] for x in window.keys()])
        while not andMapDict(termsProcessed):
            for eachTerm in blurbDict.keys():

                if not termsProcessed[eachTerm]:
                    termPosition = blurbDict[eachTerm][termWindowIndexes[eachTerm]]

                    tempWindow = {}
                    for eachT in window.keys():
                        if eachT == eachTerm:
                            tempWindow[eachT] = termPosition
                        else:
                            tempWindow[eachT] = window[eachT]
                    tempRange = minDiff([tempWindow[x] for x in tempWindow.keys()])
                    if 1 < tempRange < smallestRange:
                        window = tempWindow
                        smallestRange = tempRange


            smallestInWindow = getSmallestTermInWindow(window)
            termWindowIndexes[smallestInWindow]+=1
            if termWindowIndexes[smallestInWindow] == len(blurbDict[smallestInWindow]):
                termsProcessed[smallestInWindow] = True
                window.__delitem__(smallestInWindow)

        """
        Score Calculation
        """

        numOfContainTerms = len(blurbDict.keys())

        """
        APPROACH

        1) [average precision = 0.001] Only use the rangeOfWindow as the scores for each document.
        The smaller the rangeOfWindow is, the higher rank is achieved. Then the average precision is around 0.001.

        2) [average precision = 0.004] If a document has partial terms of the query(missing some terms),
        we give some penalty to reduce the scores, which depends how many terms are missing.
        For example, use the scores to minus numberOfTermsMissing * C, where C is a constant.
        But the result is around 0.004.

        We could use C = (avgDocLenOfCorpus*10)

        # missing terms penalty code snippet
        scoreToAdd -= (len(stemmedArray) - numOfContainTerms) * C

        3) [average precision = 0.0892] Then what if we give some rewards to the documents who
        contain more terms from the query? So if a document has more terms in the query, we will give
        some rewards to increase the scores, depending on how many terms are more. We use the formula
        as "(C-rangeOfWindow) * numOfContainTerms", where C is a constant(we set 1500 here), and
        numOfContainTerms means this document contains how many querying terms. For example, the
        query is "Information Retrieval", and document_1 only contains "information", then the
        numOfContainTerms=1. If document_2 contains "Information" and "Retrieval" then numOfContainTerms=2 etc.
        So this implementation gives us 0.08 average precision.

        # code snippet
        scoreToAdd += (C-smallestRange)*numOfContainTerms

        4) [average precision = 0.0236] If we consider the length of the documents, we tried the formula
        "(C - rangeOfWindow)/(lengthOfDocument + V)", where C is constant and V is the total distinct
        terms in the collection. The results is around 0.0236.

        5) [average precision = 0.1214] If we consider 3) and 4) together, we could get the formula "
        (C - rangeOfWindow) * numOfContainTerms / (lengthOfDocument + V)". We set C = 1500 here.
         And the final result is improved to 0.1214.
        """

        scoreToAdd = (1500 - smallestRange) * numOfContainTerms / (docLen + vocabSize)

        proximScores.update({docId: scoreToAdd})

    proximSortScores = []
    for i in proximScores.keys():
        proximSortScores.append((i, proximScores[i]))
    proximSortScores = sorted(proximSortScores, key=lambda tup: tup[1], reverse=True)
    proximSortScores = proximSortScores[:1000]
    print(proximSortScores)
    ansFile = open("solution/6-proximSolution.txt", "a")

    rank = 1
    for docScoreTuple in proximSortScores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank += 1
        ansFile.write(insertLine)

    ansFile.close()