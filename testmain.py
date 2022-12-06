import requests
import json
from collections import Counter
import pprint
import pandas as pd

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.u0OkluQ6Ks7JvSVByLv8sjhkmkTgEN7QkTEIFoGfsZ0"
apiUrl = "https://api.monday.com/v2/"
headers = {"Authorization" : apiKey}

query2 = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
data = {'query' : query2}

json_data = json.loads(requests.post(url=apiUrl, json=data, headers=headers).text)

# r = requests.post(url=apiUrl, json=data, headers=headers) # make request
# pprint.pprint(r.json())

df = pd.json_normalize(json_data['data']['boards'][0]['items'],record_path='column_values',meta=['name'])

print(df)
# json_response = r.json

# counter = Counter([item['status'] for item in json_response])

# print(counter["Initial DD"])

