# Figure out the date

import requests
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta
import telegram
from config import telegram_token

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


###########################################################

# DATE SECTION

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

# extract the initial DD deals and return a list
initial_dd_deals = dict_status_deals.get("Initial DD")

### MATCH PERSON WITH DATE OF THEIR INITIAL DD PIPELINE ###

# create a dictionary to add these deals as keys with no values ... yet
new_dict = {}
for key in initial_dd_deals:
    new_dict[key] = None

# Initialize the name_date dictionary
name_date = {}

# Get the names of the deals with the "Initial DD" status
initial_dd_deal_names = [deal for deal in dict_status_deals['Initial DD']]

# Iterate through the initial_dd_deal_names
for deal_name in initial_dd_deal_names:
    # Use the dict_deal_age dictionary to get the date for this deal
    date = dict_deal_age[deal_name][0]
    
    # Iterate through the dict_person_deals dictionary
    for person, deals in dict_person_deals.items():
        # If this person is associated with the current deal, add the date
        # to the name_date dictionary for this person
        if deal_name in deals:
            if person not in name_date:
                name_date[person] = [date]
            else:
                name_date[person].append(date)

### FIND OUT IF THE DEALS ARE OLDER THAN 48 HOURS (and flag is so)

# Get the current date and time
current_date = datetime.now()

# Create a timedelta object representing 48 hours
delta = timedelta(hours=48)

def late_dd():
    # Loop through the keys in name_date
    for key in name_date:
    # Create a counter to keep track of how many dates are older than 48 hours from current_date
        count = 0
  
        # Loop through the list of dates for the current key
        for date_string in name_date[key]:
            # Parse the date string into a datetime object
            date = datetime.strptime(date_string, '%Y-%m-%d')
    
            # Check if the date is older than 48 hours from current_date
            if date < current_date - delta:
            # If so, increment the counter
                count += 1
  
        # Print the count for the current key
        print(f"{key}: {count}")

late_dd()

def telegram_dd():
    bot = telegram.Bot(telegram_token)
    bot.send_message(chat_id=5312406635, text="Number of Initial DD older than 48 hours:", parse_mode=telegram.ParseMode.MARKDOWN)
    # Loop through the keys in name_date
    for key in name_date:
    # Create a counter to keep track of how many dates are older than 48 hours from current_date
        count = 0
  
        # Loop through the list of dates for the current key
        for date_string in name_date[key]:
            # Parse the date string into a datetime object
            date = datetime.strptime(date_string, '%Y-%m-%d')
    
            # Check if the date is older than 48 hours from current_date
            if date < current_date - delta:
            # If so, increment the counter
                count += 1
  
        # Print the count for the current key
        output = (f"{key}: {count}")
        bot.send_message(chat_id=5312406635, text=output, parse_mode=telegram.ParseMode.MARKDOWN)

telegram_dd()