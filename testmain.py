import requests
import json
import pandas as pd
from collections import defaultdict

# Import core data

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.u0OkluQ6Ks7JvSVByLv8sjhkmkTgEN7QkTEIFoGfsZ0"
apiUrl = "https://api.monday.com/v2/"
headers = {"Authorization" : apiKey}

query2 = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
data = {'query' : query2}

json_data = json.loads(requests.post(url=apiUrl, json=data, headers=headers).text)

# source: https://stackoverflow.com/questions/68076059/normalize-monday-com-api-json-output-in-python
data = [ [item['name']]+[c_v['text'] for c_v in item['column_values']] for item in json_data['data']['boards'][0]['items']]
df = pd.DataFrame(data,columns=['Deals','Person','Status','Date'])
# print(df)


###########################################################

# General Statistics

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


###########################################################

# Create a general overview of which deals are assigned to which person and the number of deals per person
# Create dictionary that assigns deals to repsective individuals and print out this overview
d = [dict(zip(["Deals", "Person"], item)) for item in data]

dict_person_deals = defaultdict(list)

for item in d:
    dict_person_deals[item['Person']].append(item['Deals'])

def count_len_dict(person):
    """
    a function that counts the number of values per key (the number of deals assigned to the person)
    """
    count = len(dict_person_deals.get(person))
    return count

# print(f"""
# \n\033[4mIndividual Pipeline:\033[0m
# Hrishi's deals:{dict_list.get('Hrishi')}
# Total deals: {count_len_dict('Hrishi')}\n
# Mads's deals:{dict_list.get('mpedersen1@babson.edu')}
# Total deals: {count_len_dict('mpedersen1@babson.edu')}\n""")


###########################################################

# create a dictionary that contains the person, the deals and the status of these deals and print out this overview
d1 = [dict(zip(["Deals", "Person","Status"], item)) for item in data]

dict_status_deals = defaultdict(list)

# Group by status by adding the deals (value) to the status (key)
for item in d1:
    dict_status_deals[item['Status']].append(item['Deals'])

def count_len_stat(status):
    """
    a function that counts the number of values per key (the number of deals assigned to the person)
    """
    count = len(dict_status_deals.get(status))
    return count

# print(f"""
# \033[4mTotal:\033[0m
# Initial DD: {count_len_stat('Initial DD')}
# Need 2nd Opinion: {count_len_stat('Need 2nd Opinion')}
# Get Intro: {count_len_stat('Get Intro')}\n""")


###########################################################

# create a dictionary that contains the person, the status of their deals, and print out this overview
d2 = [dict(zip(["Deals","Person", "Status"], item)) for item in data]

dict_person_status = defaultdict(list)

for item in d2:
    dict_person_status[item['Person']].append(item['Status'])

def count_status(person, status):
    """
    A function that counts the number of times a STATUS repeats itself in a list (value) assigned to a PERSON (key)
    """
    count = dict_person_status.get(person).count(status)
    return count

# print(f"""
# \033[4mHrishi:\033[0m
# Initial DD: {count_status('Hrishi', 'Initial DD')}
# Need 2nd Opinion: {count_status('Hrishi', 'Need 2nd Opinion')}
# Get Intro: {count_status('Hrishi', 'Get Intro')}\n
# \033[4mMads:\033[0m
# Initial DD: {count_status('mpedersen1@babson.edu', 'Initial DD')}
# Need 2nd Opinion: {count_status('mpedersen1@babson.edu', 'Need 2nd Opinion')}
# Get Intro: {count_status('mpedersen1@babson.edu', 'Get Intro')}\n
# """)



print(f"""
\033[4mIndivivdual Pipelines\033[0m\n
Hrishi:
Total Deals: {count_len_dict('Hrishi')}
Initial DD: {count_status('Hrishi', 'Initial DD')}
Get Intro: {count_status('Hrishi', 'Get Intro')}
Need 2nd Opinion: {count_status('Hrishi', 'Need 2nd Opinion')}
Deals: {dict_person_deals.get('Hrishi')}\n
Mads:
Total Deals: {count_len_dict('mpedersen1@babson.edu')}
Initial DD: {count_status('mpedersen1@babson.edu', 'Initial DD')}
Get Intro: {count_status('mpedersen1@babson.edu', 'Get Intro')}
Need 2nd Opinion: {count_status('mpedersen1@babson.edu', 'Need 2nd Opinion')}
Deals: {dict_person_deals.get('mpedersen1@babson.edu')}\n
""")


###########################################################

# Find the number of Initial DD's that are older than 48hrs:
# create a dictionary that contains the person, the status of their deals, the date of the deal and finds "Initial DD" deals 
# that are older than 48hrs and prints the total
d3 = [dict(zip(["Deals","Person", "Status", "Date"], item)) for item in data]

# create a function that filters for "Initial DD" only

dict_deal_age = defaultdict(list)

# create a function that calculate the age of a deal

def date_extractor():
    for item in d3:
        dict_deal_age[item['Deals']].append(item['Date'])

date_extractor()

print(dict_deal_age)