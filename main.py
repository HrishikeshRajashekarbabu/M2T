import requests
import json
import pandas as pd
from collections import defaultdict
from config import apiKey, apiUrl, telegram_token
from datetime import datetime, timedelta
import colorama
import io
import telegram
from contextlib import redirect_stdout

# Import core data

headers = {"Authorization" : apiKey}

query2 = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
data = {'query' : query2}

json_data = json.loads(requests.post(url=apiUrl, json=data, headers=headers).text)

# source: https://stackoverflow.com/questions/68076059/normalize-monday-com-api-json-output-in-python
data = [ [item['name']]+[c_v['text'] for c_v in item['column_values']] for item in json_data['data']['boards'][0]['items']]
df = pd.DataFrame(data,columns=['Deals','Person','Status','Date'])

# Initialize the colorama module
colorama.init()

###########################################################

# General Statistics

intial_dd_count = df['Status'].str.contains('Initial DD').sum()
get_intro_count = df['Status'].str.contains('Get Intro').sum()
opinion_count = df['Status'].str.contains('Need 2nd Opinion').sum()
schedule_call_count = df['Status'].str.contains('Schedule Call').sum()

def general_overview_print():
    print("\n\033[4mGeneral Overview\033[0m")
    print(f'Initial DD past 48 hours: {colorama.Style.BRIGHT}{colorama.Fore.RED}{counter}{colorama.Style.RESET_ALL}') # Source: https://chat.openai.com/chat
    print(f"Initial DD Count: {intial_dd_count}")
    print(f"Get Intro Count: {get_intro_count}")
    print(f"2nd Opinion Count: {opinion_count}")
    print(f"Schedule Call Count: {schedule_call_count}\n")

#######################s####################################

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

# Specify the key for the values to extract from dict_deal_age
initial_dd_keys = dict_status_deals['Initial DD']
dates_initial_dd = dict_deal_age.items()
values_initial_dd = [value for (key, value) in dates_initial_dd if key in initial_dd_keys]

# turn the above list of lists into a single list of date strings
single_value_list = []

# Using the += operator to add dates from deals in Initial DD to the above list
for sublist in values_initial_dd:
    single_value_list += sublist

# List of datetime objects
date_objects = [datetime.strptime(date_string, '%Y-%m-%d') for date_string in single_value_list]

# Get the current date and time
current_date = datetime.now()

# Find the difference between each date in the list and the current date
date_differences = [current_date - date for date in date_objects]

# Initialize a counter
counter = 0

# Iterate over the list of date differences
for date_diff in date_differences:
    # Check if the number of days in the date difference is greater than 2
    if date_diff.days >= 2:
        if date_diff.seconds > 0:
        # Increment the counter
            counter += 1

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

# telegram bot

bot = telegram.Bot(telegram_token)

updates = bot.get_updates()
print(updates)
for update in updates:
    if update.message:
        user_name = update.message.from_user.first_name
bot.send_message(chat_id = update.message.chat_id, text="Good Evening, " + user_name + "!" + "\n" + "Here are your updates for the day: ")

def telegram_dd():
    bot = telegram.Bot(telegram_token)
    bot.send_message(chat_id=update.message.chat_id, text="Number of Initial DD older than 48 hours:", parse_mode=telegram.ParseMode.MARKDOWN)
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
        bot.send_message(chat_id=update.message.chat_id, text=output, parse_mode=telegram.ParseMode.MARKDOWN)

telegram_dd()

# telegram bot message
message = "General Overview\n"
message += "Initial DD past 48 hours: {}\n".format(counter)
message += "Initial DD Count: {}\n".format(intial_dd_count)
message += "Get Intro Count: {}\n".format(get_intro_count)
message += "2nd Opinion Count: {}\n".format(opinion_count)
message += "Schedule Call Count: {}\n".format(schedule_call_count)
###############################################################

# final function that ties everything back together

def final_print():
    people = list(set(df['Person'].values.tolist()))
    # print this for the number of people listed
    num_items = len(people)
    for i in range(num_items):
        print(f"""\n\033[4m{people[i]}\033[0m\nTotal Deals: {count_len_dict(people[i])}\nInitial DD: {count_status(people[i],'Initial DD')}\nGet Intro: {count_status(people[i], 'Get Intro')}\nNeed 2nd Opinion: {count_status(people[i], 'Need 2nd Opinion')}\nDeals: {dict_person_deals.get(people[i])}\n""")

def telegram_final_print():
    people = list(set(df['Person'].values.tolist()))
    # print this for the number of people listed
    num_items = len(people)
    for i in range(num_items):
        person = people[i]
        PersonalDeals = (
            f"""{person}\033\nTotal Deals: {count_len_dict(person)}\n"""
            f"""Initial DD: {count_status(person, 'Initial DD')}\n"""
            f"""Get Intro: {count_status(person, 'Get Intro')}\n"""
            f"""Need 2nd Opinion: {count_status(person, 'Need 2nd Opinion')}\n"""
            f"""Deals: {dict_person_deals.get(person)}\n"""
        )
        bot.send_message(chat_id=update.message.chat_id, text=PersonalDeals, parse_mode=telegram.ParseMode.MARKDOWN)

# Send the table to the user
bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

# This allows me to obtain the chatID of the relevant Telegram user as long as they interact with our telegram bot: RubberBot
'''updates = bot.get_updates()
for update in updates:
    print(update)'''


if __name__ == '__main__':
    print(f"\n ~ DAILY UPDATE ~ ")
    general_overview_print()
    print("\033[4mInitial Past 48 Hours\033[0m")
    late_dd()
    final_print()
    telegram_final_print()