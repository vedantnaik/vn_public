__author__ = 'Vedant'
import math

def unigramLmJelinekMercer(queryNumber, termFreqDict, vocabSize, termTTFDict, retriever, stemmedArray):

    unigramLMJMScores = []
    totalDocLen = sum(retriever.docInfoDict.values())

    for docId in termFreqDict.keys():
        docLen = int(termFreqDict[docId][0])

        for qWord in stemmedArray:
            if qWord not in termFreqDict[docId][1].keys():
                termFreqDict[docId][1].update({qWord:0})

        unigramLMJMScore = 0
        for term in termFreqDict[docId][1].keys():
            tf = termFreqDict[docId][1][term]
            ttf = termTTFDict[term]

            corpusProbEstimate = ttf/vocabSize
            corpusProbEstimate = 0.2150536
            # corpusProbEstimate = ttf/vocabSize -> Average precision (averaged over queries) 0.0953
            # estimating various values of lambda (corpusProbEstimate)
            # 0.22 -> Average precision (non-interpolated) for all rel docs(averaged over queries) 0.1468
            # 0.25 -> Average precision (non-interpolated) for all rel docs(averaged over queries) 0.1454
            # 0.35 -> Average precision (non-interpolated) for all rel docs(averaged over queries) 0.1426
            # 0.50 -> Average precision (non-interpolated) for all rel docs(averaged over queries) 0.1396

            foreGround = tf/docLen
            temp1 = ttf - tf
            temp2 = totalDocLen - docLen
            backGround = temp1/temp2
            p_jm_val = (corpusProbEstimate * foreGround) + ((1.0 - corpusProbEstimate) * backGround)
            unigramLMJMScore += math.log(p_jm_val)

        unigramLMJMScores.append((docId,unigramLMJMScore))

    unigramLMJMScores = sorted(unigramLMJMScores, key=lambda tup: tup[1],reverse=True)
    unigramLMJMScores = unigramLMJMScores [:100]
    print(unigramLMJMScores)
    ansFile = open("solution/5-unigramLmJMSolution.txt","a")

    rank = 1
    for docScoreTuple in unigramLMJMScores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank+=1
        ansFile.write(insertLine)

    ansFile.close()
