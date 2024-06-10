COMMAND_LIST = ("\"/search\" — find TV Serials and Movies.\n"
                "\"/wishlist\" — look at your current wishlist.")

START = ("Hello! I am exam-project-bot.\n"
         "I can show you information about TV Serials and Movies,"
         "search its by the keywords and manage your wishlist!\n"
         "All data was getting from IMDb.com.\n\n"
         "Please, use the keyboard below to choose one of following actions:\n"
         f"{COMMAND_LIST}")

HELP = ("You can use the keyboard at the bottom of the screen or one of following commands:\n"
        f"{COMMAND_LIST}")

# Texts for search
ASK_SEARCH_TERM = "What are you looking for?"
WAIT_SEARCH = "Wait a few seconds..."
NOT_FOUND = "Movies not found! Try anoter request."
STOP_SEARCHING = "The search was stopped."
ADDED = "Added!"

# Texts for wishlist
YOUR_LIST = "Your wishlist:"
REMOVED = "Removed!"
CLOSED = "Wishlist closed!"
