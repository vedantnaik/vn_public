__author__ = 'Vedant'
import math
from src.GoldenRetriever import GoldenRetriever

def tfidf(queryNumber, termFreqDict, avgLenOfCorpus, termDFDict, retriever):

    tfidfScores = []

    for docId in termFreqDict.keys():
        docLen = int(termFreqDict[docId][0])

        tf_idf = 0
        for term in termFreqDict[docId][1].keys():
            tf = termFreqDict[docId][1][term]
            logTerm = math.log(len(retriever.docInfoDict.keys())/int(termDFDict[term]))
            tf_idf += ((tf / (tf + 0.5 + (1.5 * (docLen/avgLenOfCorpus)))) * logTerm)

        tfidfScores.append((docId,tf_idf))
        

    tfidfScores = sorted(tfidfScores, key=lambda tup: tup[1],reverse=True)
    tfidfScores = tfidfScores [:100]
    print(tfidfScores)
    ansFile = open("solution/2-tfidfSolution.txt","a")

    rank = 1
    for docScoreTuple in tfidfScores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank+=1
        ansFile.write(insertLine)

    ansFile.close()
