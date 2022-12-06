import requests
import json
from collections import Counter
import pprint

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.u0OkluQ6Ks7JvSVByLv8sjhkmkTgEN7QkTEIFoGfsZ0"
apiUrl = "https://api.monday.com/v2/"
headers = {"Authorization" : apiKey}

query2 = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
data = {'query' : query2}

r = requests.post(url=apiUrl, json=data, headers=headers) # make request
pprint.pprint(r.json())

# json_response = r.json

# counter = Counter([item['status'] for item in json_response])

# print(counter["Initial DD"])