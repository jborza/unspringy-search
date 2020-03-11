# Unspringy Search

This project aims at being able to search through plaintext JSON dumps of Elasticsearch database with a 'better grep' that is JSON aware.

It may not be always realistic to keep all access / application logs alive in an Elasticsearch cluster, so you may need to export them into a plain-text format and look through them later.

Note: you could also ingest the logs back into ES for a better search experience

Using the sample `kibana_sample_data_logs` data set, imported with Kibana 7.6.1 into Elasticsearch 7.6.1, 
we 

1. initially dump the data into a json file with `python index-export-json.py > kibana_sample_data_logs.json`
2. sort the json file on the timestamp with `python sort_json.py < kibana_sample_data_logs.json > logs_dataset_sorted.json`
3. (optional) split the json file into daily/hourly/minutely bucket with `python split_by_day.py` (TODO parametrize this script)
4. prepare a search query against the dataset in `search.py` and search away
