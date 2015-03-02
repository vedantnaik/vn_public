__author__ = 'Vedant'

from elasticsearch import Elasticsearch

class GoldenRetriever:

    def __init__(self, indexFileName, catalogFileName, docInfoFileName, docStatsFileName):
        # Catalog : {term : offset}
        # Document Mappings : {docid : (docName,  docLen)}
        # Each line of index is docid1 pos delta1|docid2 pos delta1 delta2
        self.catalogName = catalogFileName
        self.docstatsName = docStatsFileName
        self.docuMapName = docInfoFileName
        self.indexFileName = indexFileName

        """
        Get the document statistics
        """
        self.avgdocLength = 0
        self.docCount = 0
        self.vocabSize = 0
        with open(self.docstatsName, "r") as dsFile:
            for dsLine in dsFile:
                if dsLine.__contains__("avg_doc_length"):
                    self.avgdocLength = dsLine[:-1].split(" ")[1]
                if dsLine.__contains__("doc_count"):
                    self.docCount = dsLine[:-1].split(" ")[1]
                if dsLine.__contains__("vocab_size"):
                    self.vocabSize = float(dsLine[:-1].split(" ")[1])

        """
        Get the term catalog information
        """
        self.catalog = {}
        with open(self.catalogName, "r") as cFile:
            allContents = cFile.read()
            entryArray = allContents.split("\n")[:-1]
            for entry in entryArray:
                term, offset = entry.split(" ")
                self.catalog.update({term: offset})

        """
        Get the document information
        """
        self.docuMap = {}
        self.docInfoDict = {}
        with open(self.docuMapName, "r") as dmFile:
            allContents = dmFile.read()
            entryArray = allContents.split("\n")[:-1]
            for entry in entryArray:
                docid, docNo, docLen = entry.split(" ")
                self.docuMap.update({docid: (docNo, docLen)})
                self.docInfoDict.update({docNo : int(docLen)})



    def getVocabSize(self):
        return self.vocabSize


    # Returns the total documents in the corpus
    def getDocCount(self):
        return self.docCount

    # Returns the average document length of files in the corpus
    def getAvgDocLenOfCorpus(self):
        return self.avgdocLength

    def getTermVector(self, term):
        if self.catalog.__contains__(term):
            offset = int(self.catalog[term])
            resultDF = 0
            resultTTF = 0
            resultTF = []
            with open(self.indexFileName, "r") as indexFile:
                indexFile.seek(offset)
                postings = indexFile.readline().replace("\n", "").split("|")
                resultDF = len(postings)
                for posting in postings:
                    split_posting = posting.split(" ")
                    docid = split_posting[0]
                    docname = self.docuMap[docid][0]
                    tf = len(split_posting[1:])
                    resultTF.append((docname, tf))
                    resultTTF += tf
            return resultTF, resultDF, resultTTF
        else:
            return dict(), 0, 0


    def getAvgDocLenOfCorpus(self):
        totalCorpusLen = (sum(self.docInfoDict.values()))
        totalNum = len(self.docInfoDict.keys())
        return totalCorpusLen/totalNum


    # note: here docId is the docno in <DOCNO> tags
    def getDocLen(self, docId):
        return self.docInfoDict[docId]


    def getAllDBlocks(self, searchTerm):
        if self.catalog.__contains__(searchTerm):
            offset = int(self.catalog[searchTerm])
            with open(self.indexFileName, "r") as indexFile:
                indexFile.seek(offset)
                postings = indexFile.readline().replace("\n", "").split("|")

                blocks = {}

                for posting in postings:
                    split_posting = posting.split(" ")
                    docidEncoded = split_posting[0]
                    docidDecoded = self.docuMap[docidEncoded][0]
                    deltas = [int(x) for x in split_posting[1:]]
                    sumSoFar = 0
                    for i in range(deltas.__len__()):
                        deltas[i] += sumSoFar
                        sumSoFar = deltas[i]
                    blocks.update({docidDecoded:deltas})
                return blocks
        else:
            return []

    def getPositions(self, searchTerm, searchDocId):
        if self.catalog.__contains__(searchTerm):
            offset = int(self.catalog[searchTerm])
            with open(self.indexFileName, "r") as indexFile:
                indexFile.seek(offset)
                postings = indexFile.readline().replace("\n", "").split("|")
                for posting in postings:
                    split_posting = posting.split(" ")
                    docidEncoded = split_posting[0]
                    docidDecoded = self.docuMap[docidEncoded][0]
                    if docidDecoded == searchDocId:
                        deltas = [int(x) for x in split_posting[1:]]
                        sumSoFar = 0
                        for i in range(deltas.__len__()):
                            deltas[i] += sumSoFar
                            sumSoFar = deltas[i]
                        return deltas
        else:
            return []




# ======================= how to use this class ========================
# retObj = GoldenRetriever()
# queryTerm = "alleg"
#
# resultTF, resultDF, resultTTF = retObj.getTermVector(queryTerm)
# print(resultDF)
# print(resultTTF)
# print(resultTF)
# print(len(resultTF))
