# Import the json and requests modules
import json
import requests

# Set the API key for your Monday.com account
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.u0OkluQ6Ks7JvSVByLv8sjhkmkTgEN7QkTEIFoGfsZ0"

# Set the URL for the Monday.com API endpoint
url = 'https://api.monday.com/v2/boards/123456.json'

# Set the parameters for the API request
params = {'api_key': api_key}

# Send the API request and retrieve the response
response = requests.get(url, params=params)

# Parse the JSON data from the response
data = json.loads(response.text)

# Convert the parsed data into a dictionary
data = dict(data)

# Print the dictionary
print(data)
