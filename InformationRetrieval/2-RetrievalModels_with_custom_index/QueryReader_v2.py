import os
import time
from IR2.GoldenRetriever_v2 import GoldenRetriever
from IR2.PorterStemmer import PorterStemmer
from IR2.models.okapiBM25 import okapiBM25
from IR2.models.proximitySearch import proximitySearch
from IR2.models.unigramLmJelinekMercer import unigramLmJelinekMercer
from IR2.models.unigramLmLaplace import unigramLmLaplace
from IR2.models.TFIDF import tfidf
from IR2.models.okapiTF import okapitf
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

def clearFile(fname):
    file=open(fname,"w")
    file.seek(0)
    file.truncate()
    file.close()

if __name__ == '__main__':

    qr = QueryReader()
    p = PorterStemmer()

    clearFile("solution/1-okapiSolution.txt")
    clearFile("solution/2-tfidfSolution.txt")
    clearFile("solution/3-okapiBM25Solution.txt")
    clearFile("solution/4-unigramLmLapSolution.txt")
    clearFile("solution/5-unigramLmJMSolution.txt")
    clearFile("solution/6-proximSolution.txt")

    """
    Version 2 change:
        The initialization of GoldenRetriever will require you to send
        file names that help build the index
        - index file name
        - catalog file name
        - docInfo file name
        - docStats file name
    """
    indexName = "AP89DOC"
    indexFileName = "indexFolder/" + indexName + ".txt"
    catalogFileName = "indexFolder/" + indexName + "-catalog.txt"
    docInfoFileName = "indexFolder/" + indexName + "-docInfo.txt"
    docStatsFileName = "indexFolder/" + indexName + "-docStats.txt"

    retriever = GoldenRetriever(indexFileName, catalogFileName, docInfoFileName, docStatsFileName)
    stopWords = open(r"D:\IR-CS6200\Assg1\data\AP_DATA\stoplist.txt","r").read().split("\n")
    otherWords = ["document", "discuss", "report", "include", "describe", "identify", "predict", "cite"]
    stopWords += otherWords
    print ("stopwords - "+ stopWords.__str__())
    print ("total " + str(len(stopWords)))

    avgDocLenOfCorpus = retriever.getAvgDocLenOfCorpus()

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

            proximitySearch(queryNumber, termFreqDict, avgDocLenOfCorpus, retriever, stemmedArray, vocabSize)
            okapitf(queryNumber, termFreqDict, avgDocLenOfCorpus)
            tfidf(queryNumber, termFreqDict, avgDocLenOfCorpus, termDFDict, retriever)
            okapiBM25(queryNumber, termFreqDict, avgDocLenOfCorpus, termDFDict, retriever, queryArray)
            unigramLmLaplace(queryNumber, termFreqDict, vocabSize, stemmedArray)
            """
              NOTE: unigramLmJelinekMercer does make changes in the termFreqDict
                    [by adding tf 0 to terms in query that do not occur in the dictionary]
                    This is why we call this last.
            """
            unigramLmJelinekMercer(queryNumber, termFreqDict, vocabSize, termTTFDict, retriever, stemmedArray)


    winsound.Beep(500,1000)
    winsound.Beep(400,2000)
    winsound.Beep(500,1000)
