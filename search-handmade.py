import json
import fileinput
import re
import operator
import functools

elastic_search = {'_source': {'excludes': ['geo', 'message', 'tags', 'event', 'phpmemory']}, 
'query': {'bool': {'must': [], 
    'filter': [ {'match_all': {}}, 
                {'match_phrase': {'host': 'www.elastic.co'}}, 
                {'match_phrase': {'geo.dest': 'CN'}}, 
                {'match_phrase': {'agent': 'Firefox'}},
                {'bool': {'should': [{'match_phrase': {'machine.os': 'osx'}}, 
                    {'match_phrase': {'machine.os': 'ios'}}], 
                    'minimum_should_match': 1}}
                ],
    'must_not': [{'match_phrase': {'response': 200}}]}
}}

mysearch = {
    'all':[
        {'match_phrase': {'geo.dest': 'CN'}}, 
        {'match_phrase': {'host': 'www.elastic.co'}}, 
        {'match_regex': {'agent': 'Firefox'}},
        {'match_phrase': {'machine.os': ['osx', 'ios']}},             
        {'not_match_phrase': {'response': 200}}
    ]
}

def match_phrase(json, key, value):
    pass

operators = {
    'match_phrase': match_phrase
}

def none(iterable):
    return not any(iterable)

def get_inner(json, keys):
    for k in keys:
        json = json[k]
    return json

def make_matcher(item):
    #e.g. {'match_phrase': {'host': 'www.elastic.co'}}
    op, args = list(item.items())[0]
    if(op == 'match_phrase'):
        #args = {'host': 'www.elastic.co'}
        key, values = list(args.items())[0]
        if isinstance(values, list): # {'host': ['www.elastic.co','static.elastic.co']}
            if('.' in key): #composite expression - 'geo.dest' : 'value'
                keys = key.split('.')
                if(len(keys) == 2): # a.b
                    return lambda json: json[keys[0]][keys[1]] in values
                else: # a.b.c.d (and longer)
                    return lambda json: get_inner(json, keys) in values    
            else:
                return lambda json: json[key] in values
        if('.' in key): #composite expression - 'geo.dest' : 'value'
            keys = key.split('.')
            if(len(keys) == 2): # a.b
                return lambda json: json[keys[0]][keys[1]] == values
            elif(len(keys) == 3): # a.b.c
                return lambda json: json[keys[0]][keys[1]][keys[2]] == values
            else: # a.b.c.d (and longer)
                return lambda json: get_inner(json, keys) == values
        else: #simple expression - 'key': 'value'
            return lambda json: json[key] == values
    if(op == 'not_match_phrase'):
        key, values = list(args.items())[0]
        return lambda json: json[key] != values
    if(op == 'match_regex'):
        key, values = list(args.items())[0]
        return lambda json: re.search(values,json[key])
    raise SyntaxError('Error parsing ' + str(item))

def make_matchers(children):
    return [make_matcher(child) for child in children]

def all_match(functions):
    return lambda i: all([f(i) for f in functions])

def any_match(combined_functions):
    return lambda i: any([f(i) for f in combined_functions])

def combinator_or(f1, f2):
    return lambda x: f1(x) or f2(x)

def combinator_and(f1, f2):
    return lambda x: f1(x) and f2(x)

def reduce_functions(combinator, functions):
    return functools.reduce(combinator, functions)

def build_evaluator(node):    
    # emit 'and' for all items inside "must"
    #"must_not" -> not any (...)
    matchers = make_matchers(node['all'])
    return reduce_functions(combinator_and, matchers)

#operate on a single file
filename = 'elastic_long.json'

def match2(json, search):
    if not (re.search('www.elastic.co', json['host'])):
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


#def match_oneline(json, search):
#expected 15 results
def match_handmade(json):
    return json['response'] != 200 and re.search('www.elastic.co', json['host']) and re.search('Firefox',json['agent']) and json['machine']['os'] in ['ios', 'osx'] and json['geo']['dest'] == 'CN' 


matcher = build_evaluator(mysearch)

with open(filename,'r') as file_input:
    #for line in fileinput.input():
    for line in file_input:
        json_data = json.loads(line)
        if(matcher(json_data)):
            print(json.dumps(json_data))

