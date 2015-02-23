__author__ = 'Vedant'
import math
from src.GoldenRetriever import GoldenRetriever

def okapiBM25(queryNumber, termFreqDict, avgLenOfCorpus, termDFDict, retriever, queryArray):

    okapiBM25_Scores = []
    k1 = 1.2
    k2 = 100
    b = 0.75

    for docId in termFreqDict.keys():
        docLen = int(termFreqDict[docId][0])

        okapiBM25_score = 0
        for term in termFreqDict[docId][1].keys():

            tf_wd = termFreqDict[docId][1][term]
            totalDocCount_plus05 = len(retriever.docInfoDict.keys()) + 0.5
            df_plus05 = termDFDict[term] + 0.5

            logTerm = math.log(totalDocCount_plus05/df_plus05)
            # ... (1)

            ltNum = tf_wd + (k1 * tf_wd)
            ltDenom = tf_wd + (k1 * ((1-b) + (b * (docLen/avgLenOfCorpus))))

            large_term = ltNum/ltDenom
            # ... (2)

            tf_wq = queryArray.count(term)
            tfNum = tf_wq + (k2 * tf_wq)
            tfDenom = tf_wq + k2

            tf_term = tfNum/tfDenom
            # ... (3)

            okapiBM25_score += (logTerm * large_term * tf_term)

        okapiBM25_Scores.append((docId,okapiBM25_score))

    okapiBM25_Scores = sorted(okapiBM25_Scores, key=lambda tup: tup[1],reverse=True)
    okapiBM25_Scores = okapiBM25_Scores [:100]
    print(okapiBM25_Scores)
    ansFile = open("solution/3-okapiBM25Solution.txt","a")

    rank = 1
    for docScoreTuple in okapiBM25_Scores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank+=1
        ansFile.write(insertLine)

    ansFile.close()
