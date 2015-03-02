@echo off
>output.txt (
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 1-okapiSolution.txt
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 2-tfidfSolution.txt
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 3-okapiBM25Solution.txt
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 4-unigramLmLapSolution.txt
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 5-unigramLmJMSolution.txt
	perl trec_eval.pl qrels.adhoc.51-100.AP89.txt 6-proximSolution.txt
)