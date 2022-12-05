# import telegram
# from monday import MondayClient

# # Set up telegram bot
# bot = telegram.Bot(token='5910533175:AAHLIQvzwTut8ISC0WfMuy7VS5BuaZM8vy0')

# # Set up Monday.com client
# # monday = MondayClient(api_key='') does not work
# monday = MondayClient('eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjIwNTEwMjMyMywidWlkIjozNzEwMjA4OSwiaWFkIjoiMjAyMi0xMi0wNVQyMjoxNzo1OS4wNDlaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQzNjU4NTEsInJnbiI6InVzZTEifQ.Lz7fOIv3WG1iGxkeNrSo4n1xz0q2Vt--5y9ZvVhA2cc')

# monday.items.create_item(board_id='12345678', group_id='today',  item_name='Do a thing')

# monday.items.fetch_items_by_column_value(board_id, column_id, value)
# # Handle user input
# def handle_input(update):
#   text = update.message.text
#   user_id = update.message.from_user.id

#   # Parse user input and determine action to take
#   if text == '/create_task':
#     create_task(user_id)
#   elif text == '/view_board':
#     view_board(user_id)

# # Create a new task on Monday.com
# def create_task(user_id):
#   # Get user's workspace and board id
#   workspace = monday.workspaces.get_workspaces()
#   board_id = workspace[0]['boards'][0]['id']

#   # Create the new task
#   task_name = 'New Task'
#   task = monday.items.create_item(board_id, task_name)

#   # Send confirmation message to user
#   bot.send_message(chat_id=user_id, text="Task created successfully!")

# # View the user's Monday.com board
# def view_board(user_id):
#   # Get user's workspace and board id
#   workspace = monday.workspaces.get_workspaces()
#   board_id = workspace[0]['boards'][0]['id']

#   # Get board details
#   board = monday.boards.get_board(board_id)

#   # Send board details to user
#   bot.send_message(chat_id=user_id, text=board)

# # Set up telegram bot updates
# updater = telegram.ext.Updater(token='YOUR_TELEGRAM_BOT_TOKEN')
# updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_input))
# updater.start_polling()

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