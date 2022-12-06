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

# source: https://stackoverflow.com/questions/68076059/normalize-monday-com-api-json-output-in-python
data = [ [item['name']]+[c_v['text'] for c_v in item['column_values']] for item in json_data['data']['boards'][0]['items']]
df = pd.DataFrame(data,columns=['Deals','Person','Status','Date'])
df = df.reset_index()

intial_dd_count = df['Status'].str.contains('Initial DD').sum()
get_intro_count = df['Status'].str.contains('Get Intro').sum()
opinion_count = df['Status'].str.contains('Need 2nd Opinion').sum()
schedule_call_count = df['Status'].str.contains('Schedule Call').sum()

def general_overview_print():
    print("\n\033[4mGeneral Overview\033[0m")
    print(f"Initial DD Count: {intial_dd_count}")
    print(f"Get Intro Count: {get_intro_count}")
    print(f"2nd Opinion Count: {opinion_count}")
    print(f"Schedule Call Count: {schedule_call_count}\n")

print(general_overview_print())

groups = df.groupby("Person")
mapping = {name: group["Deals"] for name, group in groups}
print(mapping)