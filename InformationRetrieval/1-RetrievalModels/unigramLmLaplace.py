__author__ = 'Vedant'
import math

def unigramLmLaplace(queryNumber, termFreqDict, vocabSize, stemmedArray):


    unigramLMlapScores = []

    for docId in termFreqDict.keys():
        docLen = float(termFreqDict[docId][0])

        for qWord in stemmedArray:
            if qWord not in termFreqDict[docId][1].keys():
                termFreqDict[docId][1].update({qWord:0})

        unigramLMlapScore = 0

        for term in termFreqDict[docId][1].keys():
            # qWordDict[term] = 0
            tf = termFreqDict[docId][1][term]

            tfPlusOne = tf + 1.0
            docLenPlus = docLen + vocabSize
            p_laplace = tfPlusOne/docLenPlus

            # sum over all query terms
            unigramLMlapScore += math.log(p_laplace)


        unigramLMlapScores.append((docId,unigramLMlapScore))

    unigramLMlapScores = sorted(unigramLMlapScores, key=lambda tup: tup[1],reverse=True)
    unigramLMlapScores = unigramLMlapScores [:100]
    print(unigramLMlapScores)
    ansFile = open("solution/4-unigramLmLapSolution.txt","a")

    rank = 1
    for docScoreTuple in unigramLMlapScores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank+=1
        ansFile.write(insertLine)

    ansFile.close()

