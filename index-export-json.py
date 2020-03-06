from  elasticsearch import Elasticsearch
from  elasticsearch_dsl import Search
import json

es = Elasticsearch(hosts='http://localhost:9200')
index = 'kibana_sample_data_logs'

search_body = {

}

s = Search.from_dict(search_body)
s = s.using(es).index(index)

for hit in s.scan():
    print(json.dumps(hit.to_dict()))
