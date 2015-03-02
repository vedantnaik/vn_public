from time import sleep
from Tools.Scripts.treesync import raw_input
from IR2.PorterStemmer import PorterStemmer

__author__ = 'Vedant'

import re
import os

class Indexer:

    # DATA STRUCTURES:
    def __init__(self):
        self.termMap = {}       #   {term : termId}
        self.termIdMap = {}     #   {termId : term}

        self.termIdCounter = 0  #   increase this counter for every new term
        self.docuMap = {}       #   {docid : (DOC, docLen)}
        self.docIdCounter = 0   #   increase this counter for every new document

        self.perIterDocCoutner = 0
        self.perIterDict = {}   #   need to clear after every 'throttle' iterations
                                #   {termId : {docId : [list of position deltas]}}

        self.catalog = {}       #   termid : offset
        self.tmpCatalog = {}    #   termid : [list of offsets inside the temp file]

    # Method to get text in pure form without tags inside the DOC
    # Takes care of multiple TEXT tags
    def getTextFromDoc(self, docContent):
        textUnderCurrentDoc = ""
        while docContent.__len__() > 0:
            nextTextStartLocation = docContent.find('<TEXT>')
            nextTextEndLocation = docContent.find('</TEXT>')
            textUnderCurrentDoc += docContent[nextTextStartLocation+6:nextTextEndLocation].strip()
            docContent = docContent[docContent.find('</TEXT>')+7:]
        return textUnderCurrentDoc

    # Given a document number and its text,
    # index the document
    def indexDoc(self, docNo, docText, stopWordFlag, stemFlag):

        # Every document occurs once, so each will be unique
        self.docIdCounter += 1
        docId = self.docIdCounter

        position = 0    # of first word in doc

        p = PorterStemmer()
        stopWords = open(r"D:\IR-CS6200\Assg1\data\AP_DATA\stoplist.txt","r").read().split("\n")

        pattern = r'\w+(\.?\w+)*'
        regex = re.compile(pattern, re.IGNORECASE)
        docText = docText.lower()
        docText = regex.finditer(docText)

        for d in docText:
            term = d.group(0)
            position += 1

            # ignore stop words if stop word flag set
            if stopWordFlag:
                if term in stopWords:
                    continue

            # stem words if flag set
            if stemFlag:
                while term != p.stem(term, 0, len(term) - 1):
                    term = p.stem(term, 0, len(term)-1)

            # check if already exists in the termMap
            if term not in self.termMap.keys():
                self.termIdCounter+=1
                self.termMap.update({term : self.termIdCounter})
                self.termIdMap.update({self.termIdCounter : term})
            termId = self.termMap[term]

            if termId not in self.perIterDict.keys():
                # term is not in our temp dictionary
                self.perIterDict.update({termId : {docId : [position]}})
            elif docId not in self.perIterDict[termId].keys():
                # term is present in our temp dictionary, but for other documents
                self.perIterDict[termId].update({docId : [position]})
            else:
                # term is present in out temp dictionary, for this document
                # get the position of the last occurrence of the term in this document
                # to calculate the delta value
                oldPos = sum(self.perIterDict[termId][docId])
                self.perIterDict[termId][docId].append(position - oldPos)

        # add entry in docuMap
        # position will give the length of that document
        self.docuMap.update({docId : (docNo,position)})

    def documentIteration(self, indexFile):

        for termId in self.perIterDict.keys():
            startOffsetForNewTerm = indexFile.seek(0,2) # seek to EOF
            if termId not in self.tmpCatalog.keys():
                self.tmpCatalog.update({termId : [startOffsetForNewTerm]})
            else:
                self.tmpCatalog[termId].append(startOffsetForNewTerm)

            indexFile.write(termId.__str__())
            for occurranceDocid in self.perIterDict[termId].keys():
                # each document for a new term
                indexFile.write("|" + occurranceDocid.__str__() + " " +   # docid
                                self.perIterDict[termId][occurranceDocid].__str__()[1:-1].replace(",","")) # positions
            indexFile.write('\n')                       # end of line

        self.perIterDict.clear()
        self.perIterDocCoutner = 1

    def mergeToMainIndex(self, indexName, tmpIndexFile):
        indexFile = open(r"indexFolder/" + indexName + ".txt","w")
        catalogFile = open(r"indexFolder/" + indexName + "-catalog.txt","w")
        docInfoFile = open(r"indexFolder/" + indexName + "-docInfo.txt","w")
        docStatsFile = open(r"indexFolder/" + indexName + "-docStats.txt","w")

        self.catalog.clear()
        indexFile.seek(0)
        catalogFile.seek(0)
        docInfoFile.seek(0)

        tmpIndexFile.close()
        tmpIndexFile = open(tmpIndexFile.name,"r")

        docLenSum = 0
        for docidInMap in self.docuMap.keys():
            # {docid : (DOC, docLen)}
            docInfoFile.write(docidInMap.__str__() + " " +
                              self.docuMap[docidInMap][0].__str__() + " " +
                              self.docuMap[docidInMap][1].__str__() + "\n")
            docLenSum += self.docuMap[docidInMap][1]

        numberOfDocs = self.docuMap.keys().__len__()
        avgDocLen = docLenSum / numberOfDocs
        uniqueTermCount = self.tmpCatalog.keys().__len__()

        docStatsFile.seek(0)
        docStatsFile.write("avg_doc_length " + avgDocLen.__str__() + "\n" +
                           "doc_count " + numberOfDocs.__str__() + "\n" +
                           "vocab_size " + uniqueTermCount.__str__() + "\n")


        for termId in self.tmpCatalog.keys():

            iFilePosition = indexFile.tell()
            #self.catalog.update({termId:iFilePosition})
            catalogFile.write(self.termIdMap[termId].__str__() + " " + iFilePosition.__str__() + "\n") #catalog has "term<space>offset"

            termEntryInIndex = ""
            for tFileOffset in self.tmpCatalog[termId]:
                tmpIndexFile.seek(tFileOffset)
                line = tmpIndexFile.readline()
                brokenLine = line.split("|")[1:]    # exclude termId
                for dblock in brokenLine:
                    termEntryInIndex += dblock.strip()+"|"

            indexFile.write(termEntryInIndex[:-1]+"\n")         # write the line without last "|" and with "\n"




    #######################################################################################################
    # Call this function with name of index,
    # throttle = how many documents to process at a time,
    # flags to set stopping and stemming of words
    def indexCorpus(self, indexName, throttle, stopWordFlag, stemFlag):
        self.__init__()
        for dirpath, dirnames, filenames in os.walk(r"D:\IR-CS6200\Assg1\data\AP_DATA\ap89_collection"):
            # Exclude the readme file because it is not useful for querying
            allFiles = [os.path.join(dirpath, filename) for filename in filenames if filename != "readme"]

        tmpIndexFile = open(r"indexFolder/" + indexName + ".txt.tmp","w")
        for aFileName in allFiles:
            aFile = open(os.path.join(dirpath,aFileName))
            #print(aFileName.__str__())

            fileContent = aFile.read()
            docCountInFile = fileContent.count("<DOCNO>")

            while docCountInFile > 0:
                self.perIterDocCoutner += 1
                if self.perIterDocCoutner == throttle:
                    print("Index "+indexName.__str__()+"...still working...")
                    self.documentIteration(tmpIndexFile)

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

                self.indexDoc(currentDocno, currentDocText, stopWordFlag, stemFlag)

                # reduce count of docs to work on by one
                docCountInFile -= 1

        self.mergeToMainIndex(indexName, tmpIndexFile)
        print("Indexed "+indexName.__str__())



############ MAIN ##############
# i = Indexer()
import timeit

startTime = timeit.default_timer()
i.indexCorpus("AP89DOC",1000,True,True)
i.indexCorpus("AP89DOC-Stop-NoStem",1000,True,False)
i.indexCorpus("AP89DOC-NoStop-Stem",1000,False,True)
i.indexCorpus("AP89DOC-NoStop-NoStem",1000,False,False)
endTime = timeit.default_timer()
duration = (endTime - startTime)/60
print(" Total = " + str(duration))
