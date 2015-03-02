__author__ = 'Vedant'

def okapitf(queryNumber, termFreqDict, avgLenOfCorpus):

    okapiScores = {}

    for docId in termFreqDict.keys():
        docLen = int(termFreqDict[docId][0])

        okapitf_w_d = 0
        for term in termFreqDict[docId][1].keys():
            tf = termFreqDict[docId][1][term]
            dVal = docLen/avgLenOfCorpus
            denom = tf + 0.5 + 1.5*dVal
            okapitf_w_d += tf / denom

        okapiScores.update({docId : okapitf_w_d})

    okapiSortScores = []
    for i in okapiScores.keys():
        okapiSortScores.append((i,okapiScores[i]))
    okapiSortScores = sorted(okapiSortScores, key=lambda tup: tup[1],reverse=True)
    okapiSortScores = okapiSortScores [:100]
    print(okapiSortScores)
    ansFile = open("solution/1-okapiSolution.txt","a")

    rank = 1
    for docScoreTuple in okapiSortScores:
        insertLine = queryNumber.__str__() \
                     + " Q0 " + docScoreTuple[0].__str__() \
                     + " " + rank.__str__() \
                     + " " + docScoreTuple[1].__str__() \
                     + " Exp" + "\n"
        rank+=1
        ansFile.write(insertLine)

    ansFile.close()