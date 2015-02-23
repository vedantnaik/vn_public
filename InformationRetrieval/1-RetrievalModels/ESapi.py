
from src.Indexer import Indexer

__author__ = 'Vedant'

from elasticsearch import Elasticsearch

es = Elasticsearch()

indexName = "ap_dataset"
docTypeName = "document"

es.indices.delete(index=indexName, ignore=[404,400])

es.indices.create(
    index=indexName,
    body={
        "settings": {
            "index": {
                "store": {
                    "type": "default"
                },
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "analysis": {
                "analyzer": {
                    "my_english": {
                        "type": "english",
                        "stopwords_path" : "stoplist.txt"
                    }
                }
            }
        },
        "mappings" : {
            docTypeName : {
                "properties" : {
                     "text" : {
                        "type" : "string",
                        "store": True,
                        "index" : "analyzed",
                        "term_vector": "with_positions_offsets_payloads",
                        "analyzer": "my_english"
                    }
                }
            }
        }
    }
)


es.indices.refresh(index=indexName)

es.put_script(lang="groovy",id="getTF",
              body={
                  "script": "_index[field][term].tf()"
              })

es.put_script(lang="groovy",id="getDF",
              body={
                  "script": "_index[field][term].df()"
              })

es.put_script(lang="groovy",id="getTTF",
              body={
                  "script": "_index[field][term].ttf()"
              })


Indexer().demo()
Indexer().makeDocInfoFile()
