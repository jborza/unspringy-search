import json

data = []

with open('10k.json','r') as fp:
    for line in fp:
        json_data = json.loads(line)
        data.append(json_data)

data_sorted = sorted(data, key=lambda i: i['@timestamp'])

for out_data in data_sorted:
    print(json.dumps(out_data))