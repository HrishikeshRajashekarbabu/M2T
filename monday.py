# Import the necessary modules and classes
from monday import Client

# Initialize the Client object with your API key
monday = Client(api_key="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wNDlaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.Lz7fOIv3WG1iGxkeNrSo4n1xz0q2Vt--5y9ZvVhA2cc")

# Fetch the list of boards in your account
boards = monday.boards.get_all()

# Iterate over the list of boards
for board in boards:
    # Fetch the list of items on the board
    items = board.items.get_all()

    # Iterate over the list of items
    for item in items:
        # Fetch the details of the item
        item_details = item.get()

        # Print the item's name and description
        print(f"Item: {item_details.name}")
        print(f"Description: {item_details.description}")