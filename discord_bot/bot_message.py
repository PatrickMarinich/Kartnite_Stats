#Patrick Marinich
#December 2025

#contains functions that when called will prompt the discord bot to send a message to the specfied channel
#the functions in this file should be called by functions that desire this functionality

import requests
import os
from dotenv import load_dotenv

#function to allow python to start the sending of a message through the bot
#this will be useful for testing, however likely not useful for actual deployment.
def message_post_to_test_server(message):
    #read in token and test_server_channel
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID = os.getenv("TEST_SERVER_GENERAL_ID")


    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
    }
    data = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send the message.")
        print(response.text)


#function to allow python to start the sending of a message through the bot
#this will be useful for testing, however likely not useful for actual deployment.
def message_post_to_kartnite_server(message):
    #read in token and test_server_channel
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID = os.getenv("KARTNITE_SERVER_BOT_COMMANDS_ID")


    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
    }
    data = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send the message.")
        print(response.text)

#A silly main for testing
if __name__ == "__main__":
    message_post_to_test_server("This is a test message from the server! It is meant for pat's testing server")
    message_post_to_kartnite_server("This is a test message from the server! It is meant for Kartnite")