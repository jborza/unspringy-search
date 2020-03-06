#splits a json file with @timestamp field into a many files with messages grouped by the minutes

import json
import fileinput
import datetime

output_prefix = 'logs-'

data_by_minutes = {}

with open('logs_dataset_sorted.json','r') as fp:
#for line in fileinput.input():
    for line in fp:
        json_data = json.loads(line)
        timestamp = json_data['timestamp']    
        timestamp = timestamp.replace(':','')
        #nanoseconds ignored, hoping they'd be zeroes
        #date = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H%M%S.%f000%z")
        date = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H%M%S.%fZ")
        key = date.strftime('%Y-%m-%d')
        if key not in data_by_minutes:
            data_by_minutes[key] = []
        data_by_minutes[key].append(json_data)
        
for key in data_by_minutes:
    with open(output_prefix+key+'.json','w') as outfile:
        for data in data_by_minutes[key]:
            outfile.write(json.dumps(data))
            outfile.write('\n')       