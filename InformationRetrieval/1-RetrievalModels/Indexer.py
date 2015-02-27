from time import time
from src.PorterStemmer import PorterStemmer

_author_ = 'vedant'

import re
import os
from elasticsearch import Elasticsearch

class Indexer:

    def makeDocInfoFile(self):
        es = Elasticsearch()
        indexName = "ap_dataset"
        docTypeName = "document"
        docinfoFile = open("data/docinfo.txt","w")

        temp = es.search(index=indexName,doc_type=docTypeName,
                         body={
                             "query" : {
                                 "match_all" : {}
                             },
                             "fields": [],
                             "size": 85000
                         })

        for i in range(len(temp["hits"]["hits"])):
            currentDocno = str(temp["hits"]["hits"][i]["_id"])

            currentDocTV = es.termvector(index=indexName,doc_type=docTypeName,id=currentDocno,
                                         body={
                                             "fields" : ["text"]
                                         })
            try:
                termArray = currentDocTV["term_vectors"]["text"]["terms"]

                docLen = 0
                for termInCurr in termArray:
                    docLen += termArray[termInCurr]["term_freq"]

                print("put in file : " + currentDocno + " " + docLen.__str__())
                docinfoFile.write(currentDocno + " " + docLen.__str__() + "\n")
            except:
                docinfoFile.write(currentDocno + " 0\n")
                print("put in file : " + currentDocno + " 0")
                continue


    def getTextFromDoc(self, docContent):
        textUnderCurrentDoc = ""
        while docContent.__len__() > 0:
            nextTextStartLocation = docContent.find('<TEXT>')
            nextTextEndLocation = docContent.find('</TEXT>')
            textUnderCurrentDoc += docContent[nextTextStartLocation+6:nextTextEndLocation].strip()
            docContent = docContent[docContent.find('</TEXT>')+7:]
        return textUnderCurrentDoc


    def demo(self):
        for dirpath, dirnames, filenames in os.walk(r"D:\IR-CS6200\Assg1\data\AP_DATA\ap89_collection"):
            # Exclude the readme file because it is not useful for querying
            allFiles = [os.path.join(dirpath, filename) for filename in filenames if filename != "readme"]

        stopWords = open(r"D:\IR-CS6200\Assg1\data\AP_DATA\stoplist.txt","r").read().split("\n")

        es = Elasticsearch()
        indexName = "ap_dataset"
        docTypeName = "document"

        for aFileName in allFiles:
            aFile = open(os.path.join(dirpath,aFileName))
            fileContent = aFile.read()

            docCount = fileContent.count("<DOCNO>")

            while docCount > 0:
                # get document number of first doc in file content,
                nextDocnumStartLocation = fileContent.find('<DOCNO>')
                nextDocnumEndLocation = fileContent.find('</DOCNO>')
                currentDocno = fileContent[nextDocnumStartLocation+7:nextDocnumEndLocation].strip()

                # remove that part from the file content
                fileContent = fileContent[nextDocnumEndLocation+8:]

                # get rest of doc content of the first doc in docContent
                docContent = fileContent[:fileContent.find('</DOC>')]
                docContent = docContent.replace('\n',' ')

                # extract text from the docContent
                currentDocText = self.getTextFromDoc(docContent)
                
                print("indexing document number - " + currentDocno + " " +docCount.__str__())
                es.index(index=indexName,
                         doc_type=docTypeName,
                         id= currentDocno,
                         body={"doc_no" : currentDocno,
                               "text" : currentDocText})

                # reduce count of docs to work on by one
                docCount -= 1

        print("part 1 done")


Indexer().demo()
Indexer().makeDocInfoFile()

print("all done")
