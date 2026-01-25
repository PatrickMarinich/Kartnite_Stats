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

#locks for specific commands
time_trial_user_lock = 0

# Define the bot and its command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # intents=discord.Intents.all() covers all necessary intents

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
async def tt_track_stats(ctx,track=None):
    """Expects an argument <track>, provides current TT leaderboards""" 

    if track not in TIME_TRIAL_TRACKS and track not in TRACK_NICKNAME_LIST.keys():
        await ctx.send('Please Provide a valid track')
        return -1
    #if nickname replace
    if track in TRACK_NICKNAME_LIST.keys():
        track = TRACK_NICKNAME_LIST[track]

    #calculate all the history information
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}
    all_histories_nsc = {}

    #data is now in the format of: 
    #{player : {track: (time, date_set), ...}, ...}
    for player in players:
        all_histories[player] = convert_history_to_dict(player)
        all_histories_nsc[player] = convert_nsc_history_to_dict(player)

    #if the track has a sc, print it, otherwise ignore
    if track in TIME_TRIAL_SHORTCUT_TRACKS:
        shortcut = get_current_leaderboard(all_histories, track, category='open')
        non_shortcut = get_current_leaderboard(all_histories_nsc, track)

        output_str = f'Non-Shortcut Leaderboard for {track}\n'
        output_str += non_shortcut.to_markdown(index=False) + "\n\n"
        output_str += f'Shortcut Leaderboard for {track}\n'
        output_str += shortcut.to_markdown(index=False)

        await ctx.send(output_str)

    else:
        non_shortcut = get_current_leaderboard(all_histories, track, category='open')
        output_str = f'Non-Shortcut Leaderboard for {track}\n\n'
        output_str += non_shortcut.to_markdown(index=False)
        await ctx.send(output_str)

    
    return 0

@bot.command()
async def generate_time_trials(ctx, player=None):
    """Expects an argument <player>, Generates the Time Trial PDF for <player>"""

    #check if the lock is set, if so return a failure, otherwise take the lock
    global time_trial_user_lock
    if time_trial_user_lock == 1:
        await ctx.send('Somebody else is currently generating a Time Trials PDF, please wait until they are done.')
        return -1
    else:
        #set the lock to 1, remove lock at all exit points
        time_trial_user_lock = 1

    #runs the creation of the TimeTrials
    if player in TIME_TRIAL_PLAYERS:
        await ctx.send('Attempting to update the database, this may take up to a minute...')
        #first parse the google_sheets
        try:
            updated = parse_google_sheets.main()
        except Exception as e:
            print(e)
            await ctx.send("ERROR: Parsing the google sheets produced an error, contact pat")
            time_trial_user_lock = 0
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
            time_trial_user_lock = 0
            return -1
        
        await ctx.send('Generating the Time Trials PDF, this should be fast!')
        try:
            generatedFile = time_trial_profile.convertHTMLtoPDF(HTML)
            await ctx.send('Success: PDF was generated successfully')
        except Exception as e:
            print(e)
            await ctx.end("ERROR: PDF failed to generate, contact pat")
            time_trial_user_lock = 0
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
    #remove the lock
    time_trial_user_lock = 0
    return 0

# Run the bot with the token
bot.run(TOKEN)