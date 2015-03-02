=====================================================================
	    WELCOME TO VERSION 2 OF OUR RETREIVAL MODEL
=====================================================================
Updates:
- Indexing is done without elasticsearch; i.e. custom index is built
- Proximity Search is implemented
- Code has been cleaned up and modified to use the new custom index

=====================================================================
HOW TO EXECUTE:
=====================================================================

Following is the order in which the files should be executed:
1. Indexer_v2.py
   Q. How to use this file?
-> 1. Import Indexer from Indexer_v2
   2. Create object -
		i = Indexer()
   3. Invoke indexer
	i.indexCorpus(indexName, throttle, stopWordFlag, stemFlag)
		- indexName is a String
		- throttle is an int and tells how many documents to 
		index in one iteration
		- stopWordFlag is a boolean and tells whether to remove
		stop words during indexing
		- stemFlag is a boolean and tells whether to stem words
		during indexing
	[The corpus location is hard-coded to 
	"D:\IR-CS6200\Assg1\data\AP_DATA\ap89_collection"]
3. QueryReader_v2.py
   Q. How to use this file?
-> 1. Run this to execute all queries within the file
	"D:\IR-CS6200\Assg1\data\AP_DATA\query_desc.51-100.short.txt"


=====================================================================
FOLDERS:
=====================================================================

"models"
- Contains the code for various models that have been implemented
- "okapiTF"
- "TFIDF"
- "okapiBM25"
- "unigramLmLaplace"
- "unigramLmJelinekMercer"
- "proximitySearch"
  NOTE: unigramLmJelinekMercer does make changes in the termFreqDict
	[by adding tf 0 to terms in query that do not occur in the dictionary]
	This is why we call this last.

"solution"
- Contains solutions to each language model
- run-trec-eval.bat:
	Run to compare results using trec-eval
	Output will be stored in output.txt in the same folder

"indexFolder"	[NOT INCLUDED IN THIS PACKAGE]
- Contains files required by the scoring functions
- These files are generated during the indexing
- Files are
	-	<indexName>.txt		- the index file
	-	<indexName>-catalog	- "term termId" mapping
	-	<indexName>-docInfo	- "docid docNO docLen" mapping
	-	<indexName>-docStats	- "avg_doc_length doc_count vocab_size" 
					of corpus

=====================================================================
PYTHON FILES:
=====================================================================

"Indexer_v2"
- Indexes the data files into custom index based on given parameters
- Prepares files within indexFolder

"GoldenRetriever_v2"
- Retrieves information from index created by Indexer_v2

"PorterStemmer"
- Used to stem query words

"QueryReader_v2"
- Reads queries from specified path and stores results in "solution" folder
- Uses GoldenRetriever_v2 to get information from index created by Indexer_v2
- Result for specific language model can be obtained by commenting out 
  lines to call other LMs
