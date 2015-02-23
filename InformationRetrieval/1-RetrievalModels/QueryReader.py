import os
import time
from src.GoldenRetriever import GoldenRetriever
from src.PorterStemmer import PorterStemmer
from src.okapiBM25 import okapiBM25
from src.unigramLmJelinekMercer import unigramLmJelinekMercer
from src.unigramLmLaplace import unigramLmLaplace
from src.TFIDF import tfidf
from src.okapiTF import okapitf
import winsound

__author__ = 'Vedant'


class QueryReader:
    '''
    Given a query line from the query file,
    this function will return an array such that
    [0] = query number
    [1] onwards = query terms
    <note: the query terms will be stemmed and will not include stop words>
    '''
    def giveNextQuery(self, queryLine, stopWords):

        rawArray = queryLine.replace(".","").replace(",","").replace('"',"").replace("\n", "").replace("-", " ") \
            .replace("(", "").replace(")", "").split(" ")

        for item in stopWords:
            while item in rawArray: rawArray.remove(item)

        originalArray = rawArray.copy()

        toStemArray = rawArray
        p = PorterStemmer()
        for i in range(toStemArray.__len__()):
            if i != 0:
                while toStemArray[i] != p.stem(toStemArray[i],0,len(toStemArray[i])-1):
                    toStemArray[i] = p.stem(toStemArray[i],0,len(toStemArray[i])-1)

        return (rawArray[0],originalArray[1:], toStemArray[1:])


if __name__ == '__main__':

    qr = QueryReader()
    p = PorterStemmer()

    file=open(r"solution/1-okapiSolution.txt","w")
    file.seek(0)
    file.truncate()
    file.close()
    file=open(r"solution/2-tfidfSolution.txt","w")
    file.seek(0)
    file.truncate()
    file.close()
    file=open(r"solution/3-okapiBM25Solution.txt","w")
    file.seek(0)
    file.truncate()
    file.close()
    file=open(r"solution/4-unigramLmLapSolution.txt","w")
    file.seek(0)
    file.truncate()
    file.close()
    file=open(r"solution/5-unigramLmJMSolution.txt","w")
    file.seek(0)
    file.truncate()
    file.close()

    retriever = GoldenRetriever()
    stopWords = open(r"D:\IR-CS6200\Assg1\data\AP_DATA\stoplist.txt","r").read().split("\n")
    otherWords = ["document", "discuss", "report", "include", "describe", "identify", "predict", "cite"]
    stopWords += otherWords
    print ("stopwords - "+ stopWords.__str__())
    print ("total " + str(len(stopWords)))

    avgDocLenOfCorpus = retriever.getAvgDocLenOfCorpus()

    # trying given value on piazza post cid=56
    # vocabSize = 20000.0
    vocabSize = retriever.getVocabSize()
    print("Size of vocabulary " + vocabSize.__str__())
    print("average doc len of entire corpus = " + avgDocLenOfCorpus.__str__())

    queryFile = open(r"D:\IR-CS6200\Assg1\data\AP_DATA\query_desc.51-100.short.txt","r")
    for line in queryFile:
        termFreqDict = {}
        termDFDict = {}
        termTTFDict = {}

        if line != "\n" and line != "":
            print(line)
            queryNumber, queryArray, stemmedArray = qr.giveNextQuery(line.lower(),stopWords)

            print(queryNumber, queryArray)
            #for term in queryArray:
            for term in stemmedArray:
                print("processing "+ term)
                resultTF, resultDF, resultTTF = retriever.getTermVector(term)

                # CODE TO STORE TTF OF TERMS
                if term not in termTTFDict.keys():
                    termTTFDict.update({term : resultTTF})

                # CODE TO STORE DF OF TERMS
                if term not in termDFDict.keys():
                    termDFDict.update({term : resultDF})

                for docId, docTermFreq in resultTF:
                    docLen = retriever.docInfoDict[docId]
                    if docId in termFreqDict.keys():
                        termFreqDict[docId][1].update({term : docTermFreq})
                    else:
                        termFreqDict.update({docId : (docLen, {term : docTermFreq})})

            okapitf(queryNumber, termFreqDict, avgDocLenOfCorpus)
            tfidf(queryNumber, termFreqDict, avgDocLenOfCorpus, termDFDict, retriever)
            okapiBM25(queryNumber, termFreqDict, avgDocLenOfCorpus, termDFDict, retriever, queryArray)
            unigramLmLaplace(queryNumber, termFreqDict, vocabSize, stemmedArray)
            unigramLmJelinekMercer(queryNumber, termFreqDict, vocabSize, termTTFDict, retriever, stemmedArray)

    winsound.Beep(500,1000)
    winsound.Beep(400,2000)
    winsound.Beep(500,1000)
