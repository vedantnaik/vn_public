=====================================================================
HOW TO EXECUTE:
=====================================================================

Following is the order in which the files should be executed:
1. ESapi.py
2. Indexer.py
....................................[SUBMISSION CHECKLIST].........(indexer’s source code)
3. QueryReader.py
....................................[SUBMISSION CHECKLIST].........(query program’s source code)


=====================================================================
FOLDERS:
=====================================================================

"solution"
- Contains solutions to each language model
....................................[SUBMISSION CHECKLIST].........(results)

"data"
- Contains files required by the scoring functions
- "docinfo" file is generated during indexing


=====================================================================
PYTHON FILES:
=====================================================================

"ESapi"
- form/setup index in elasticsearch

"Indexer"
- indexes the data files into created index
- prepares docinfo file

"GoldenRetriever"
- Retrieves information from elasticsearch

"PorterStemmer"
- used to stem query words

"QueryReader"
- Reads querys from specified path and stores results in "solution" folder
- Result for specific language model can be obtained by commenting out 
  lines to call other LMs

[Rest of the files each contain code for scoring using various language models]
- "okapiTF"
- "TFIDF"
- "okapiBM25"
- "unigramLmLaplace"
- "unigramLmJelinekMercer"
