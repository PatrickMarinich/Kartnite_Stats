#Patrick Marinich
#December 29th 2025
#Create a discord bot that can perform actions.

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys

#import the constants file
from constants import *

#to allow imports from time_trials and versus_races
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from time_trials import parse_google_sheets
from time_trials import time_trial_profile
from time_trials.time_trial_stats import *

# Load the token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the bot and its command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # intents=discord.Intents.all() covers all necessary intents

#define an empty set to track active users. ##TODO: more here...
bot.current_users = set()
######


@bot.event
async def on_ready():
    """Prints a message when the bot successfully connects."""
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    """A simple command that responds with 'Pong!'"""
    await ctx.send('Pong!')

@bot.command()
async def generate_time_trials(ctx, player=None):
    """Expects an argument <player>, Generates the Time Trial PDF for <player>"""
    #runs the creation of the TimeTrials
    if player in TIME_TRIAL_PLAYERS:
        await ctx.send('Attempting to update the database, this may take up to a minute...')
        #first parse the google_sheets
        try:
            updated = parse_google_sheets.main()
        except Exception as e:
            print(e)
            await ctx.send("ERROR: Parsing the google sheets produced an error, contact pat")
            return -1
        if updated == 1:
            await ctx.send('Success: database update was successful!')
        else:
            await ctx.send('Success: No update was necessary!')

        
        #attempt to generate the HTML for the PDF
        await ctx.send('Generating the Time Trials HTML, this may take up to a minute...')
        try:
            HTML = time_trial_profile.create_time_trial_profile(player)
            await ctx.send('Success: HTML was generated successfully')
        except Exception as e:
            print(e)
            await ctx.send("ERROR: HTML failed to generate, contact pat") 
            return -1
        
        await ctx.send('Generating the Time Trials PDF, this should be fast!')
        try:
            generatedFile = time_trial_profile.convertHTMLtoPDF(HTML)
            await ctx.send('Success: PDF was generated successfully')
        except Exception as e:
            print(e)
            await ctx.end("ERROR: PDF failed to generate, contact pat")
            return -1
        
        #if we made it this far, attach the file!
        gfile = discord.File(generatedFile)
        await ctx.send(f"Success: Attached is the time trial pdf for {player}", file=gfile)
        
        #once the file has been sent, clean up the directory by removing the files
        if os.path.exists(generatedFile):
            os.remove(generatedFile)
            print(f"{generatedFile} has been deleted.")
        else:
            print(f"The file {generatedFile} does not exist.")

        if os.path.exists(player+".html"):
            os.remove(player+".html")
            print(f"{player+".html"} has been deleted.")
        else:
            print(f"The file {player+".html"} does not exist.")


    else:
        await ctx.send(f"please use !generate_time_trials <player>\n Current Players TT supports: {TIME_TRIAL_PLAYERS}\n Please ensure spelling and capitalization match")


import requests

# Run the bot with the token
bot.run(TOKEN)