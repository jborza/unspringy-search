import json
import fileinput
import re

search = {'_source': {'excludes': ['geo', 'message', 'tags', 'event', 'phpmemory']}, 
'query': {'bool': {'must': [], 
'filter': [{'match_all': {}}, {'match_phrase': {'host': 'www.elastic.co'}}, {'match_phrase': {'geo.dest': 'CN'}}, {'match_phrase': {'agent': 'Firefox'}}, {'bool': {'should': [{'match_phrase': {'machine.os': 'osx'}}, {'match_phrase': {'machine.os': 'ios'}}], 'minimum_should_match': 1}}], 'must_not': [{'match_phrase': {'response': 200}}]}}}

simple_search = {}

#operate on a single file
filename = 'elastic_long.json'

def match(json, search):
    # if not (re.search('www.elastic.co', json['host'])):
    if not json['host'] == 'www.elastic.co':
        return False
    if not (re.search('Firefox',json['agent'])):
        return False
    if not (json['machine']['os'] in ['ios', 'osx']):
        return False
    if (json['geo']['dest'] != 'CN'):
        return False
    if(json['response'] == 200):
        return False
    return True

with open(filename,'r') as file_input:
    #for line in fileinput.input():
    for line in file_input:
        json_data = json.loads(line)
        if(match(json_data, search)):
            print(json.dumps(json_data))

