__author__ = 'Vedant'

from elasticsearch import Elasticsearch

class GoldenRetriever:

    def __init__(self):
        self.docInfoDict = {}
        docinfoFile = open("data/docinfo.txt","r")
        docinfoFileContent = docinfoFile.read().split("\n")
        docinfoFileContent = docinfoFileContent[:-1]

        for docinfoFileLine in docinfoFileContent:
            docNo, docLen = docinfoFileLine.split(" ")
            docLen = docLen.split(".")[0]
            self.docInfoDict.update({docNo : int(docLen)})

    def getVocabSize(self):
        es = Elasticsearch()
        indexName = "ap_dataset"

        result = es.search(index=indexName,
                           body={
                               "aggs" : {
                                   "unique_terms" : {
                                       "cardinality": {
                                           "field": "text"
                                       }
                                   }
                               }
                           })
        print(result["aggregations"]["unique_terms"]["value"])
        return result["aggregations"]["unique_terms"]["value"]

    def getTermVector(self, term):
        es = Elasticsearch(timeout=5000)
        indexName = "ap_dataset"
        docTypeName = "document"

        temp = es.search(index=indexName,doc_type=docTypeName,
                         body={
                             "query": {
                                 "function_score": {
                                     "query": {
                                         "match": {
                                             "text": term
                                         }
                                     },
                                     "functions": [
                                         {
                                             "script_score": {
                                                 "script_id": "getTF",
                                                 "lang" : "groovy",
                                                 "params": {
                                                     "term": term,
                                                     "field": "text"
                                                 }
                                             }
                                         }
                                     ],
                                     "boost_mode": "replace"
                                 }
                             },
                             "size": 85000,
                             "fields": ["_id"],
                             "min_score": 0.009
                         })

        resultDF = temp["hits"]["total"]
        resultTTF = 0
        resultTF = []
        for i in range(len(temp["hits"]["hits"])):
            eachDocId = temp["hits"]["hits"][i]["_id"]
            docTF =  temp["hits"]["hits"][i]["_score"]
            resultTTF += docTF
            resultTF.append((eachDocId,docTF))

        return resultTF, resultDF, resultTTF

    def getAvgDocLenOfCorpus(self):
        totalCorpusLen = (sum(self.docInfoDict.values()))
        totalNum = len(self.docInfoDict.keys())
        return totalCorpusLen/totalNum

    def getDocLen(self, docId):
        return self.docInfoDict[docId]



# ======================= how to use this class ========================
# retObj = GoldenRetriever()
# queryTerm = "alleg"
#
# resultTF, resultDF, resultTTF = retObj.getTermVector(queryTerm)
# print(resultDF)
# print(resultTTF)
# print(resultTF)
# print(len(resultTF))
