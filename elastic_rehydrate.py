import requests
import fileinput

url = 'http://localhost:9200/myindex/_doc'
headers = {'Content-type': 'application/json'}

for line in fileinput.input():
    response = requests.post(url, data=line, headers=headers)
    print(response.text)
