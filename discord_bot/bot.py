#Patrick Marinich
#December 29th 2025
#Create a discord bot that can perform actions.

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import sys
import csv

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
sync_lock = 0

# Define the bot and its command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # intents=discord.Intents.all() covers all necessary intents

######

#ctx.author.name

async def increment_stats(id):
    """Store stats of times the bot is invoked"""
    id = str(id) #convert from int to string
    data_dict = {}
    with open(STATS_TXT, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Skip the header row if present
        for key, value in reader:
            data_dict[key] = value
    file.close()
    
    #increment the counter
    if id in data_dict.keys():
        data_dict[id] = str(int(data_dict[id]) + 1)
    else:
        data_dict[id] = 1
    
    with open(STATS_TXT, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Key', 'Value'])
        # Write the key-value pairs as data rows
        for key, value in data_dict.items():
            writer.writerow([key, value])

    return 0


@bot.event
async def on_ready():
    """Prints a message when the bot successfully connects."""
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def score_help(ctx):
    """A command to return a string with kartnite score info"""
    output_str =  "Kartnite Score is defined as:\n"
    output_str += "     1 Point Per Day in First\n"
    output_str += "     0.2 Points Per Day in Second\n"
    output_str += "     0.04 Points Per Day in Third\n"
    output_str += "Scores are calculated per track\n"
    output_str += "Scores are updated at 5:15 am\n"
    await ctx.send(output_str)
    await increment_stats(ctx.author.id)

@bot.command()
async def sync(ctx):
    """Allows a discord user to update the database if something was entered into the google sheet"""
    #check if the lock is set, if so return a failure, otherwise take the lock
    global sync_lock

    if sync_lock == 1:
        await ctx.send('Somebody else is currently syncing the database, try again later')
        return -1
    else:
        #set the lock to 1, remove lock at all exit points
        sync_lock = 1

    await ctx.send('Attempting to update the database, this may take up to a minute...')
    #first parse the google_sheets
    try:
        updated = parse_google_sheets.main()
    except Exception as e:
        print(e)
        await ctx.send("ERROR: Parsing the google sheets produced an error, contact pat")
        sync_lock = 0
        return -1
    if updated == 1:
        await ctx.send('Success: database update was successful!')
    else:
        await ctx.send('Success: No update was necessary!')

    sync_lock = 0

    await increment_stats(ctx.author.id)
    return 0

    

@bot.command()
async def tt_track_player(ctx, track = None, player_in = None): 
    """Expects arguments of <track> <player>, returns players tt stats on the track"""
    #make sure track makes sense
    if track not in TIME_TRIAL_TRACKS and track not in TT_TRACK_NICKNAME_LIST.keys():
        await ctx.send('Please Provide a valid track')
        return -1
    #if nickname replace
    if track in TT_TRACK_NICKNAME_LIST.keys():
        track = TT_TRACK_NICKNAME_LIST[track]

    #make sure player makes sense
    if player_in not in TIME_TRIAL_PLAYERS:
        await ctx.send('Please Provide a valid player name, (hint: captalize the first letter)')
        return -1
    
    #calculate all the history information
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}
    all_histories_nsc = {}
    for player in players:
        all_histories[player] = convert_history_to_dict(player)
        all_histories_nsc[player] = convert_nsc_history_to_dict(player)

    if track in TIME_TRIAL_SHORTCUT_TRACKS:
        
        #DO NSC FIRST
        pb = get_player_current_pb(player_in, all_histories_nsc, track)
        date = get_player_current_pb_date(player_in, all_histories_nsc, track)
        standard = get_player_current_standard(player_in, all_histories_nsc, track)
        score = get_player_track_score(player_in, all_histories_nsc, track)
        placement = get_placements(all_histories_nsc,player_in,track)

        pb_history = get_player_line_graph(player_in, all_histories_nsc, track, extra_txt='nsc')

        output_string = f"{player_in}'s stats for {track} - NSC\n"
        output_string += f'Current PB: {pb} \n'
        output_string += f'Leaderboard Position: {placement} \n'
        output_string += f'Current Standard: {standard} \n'
        output_string += f'Date Set: {date} \n'
        output_string += f'Kartnite Score: {score} \n'
        await ctx.send(output_string)

        #include the record timeline
        file = discord.File(pb_history, filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(f"{player_in}'s NSC Personal Best Timeline", file=file, embed=embed)

        #then compute the sc stats
        pb = get_player_current_pb(player_in, all_histories, track)
        date = get_player_current_pb_date(player_in, all_histories, track)
        standard = get_player_current_standard(player_in, all_histories, track)
        score = get_player_track_score(player_in, all_histories, track)
        placement = get_placements(all_histories,player_in,track)

        pb_history = get_player_line_graph(player_in, all_histories, track, extra_txt='nsc')

        output_string = f"\n{player_in}'s stats for {track} - SC\n"
        output_string += f'Current PB: {pb} \n'
        output_string += f'Leaderboard Position: {placement} \n'
        output_string += f'Current Standard: {standard} \n'
        output_string += f'Date Set: {date} \n'
        output_string += f'Kartnite Score: {score} \n'
        await ctx.send(output_string)

        #include the record timeline
        file = discord.File(pb_history, filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(f"{player_in}'s SC Personal Best Timeline", file=file, embed=embed)



    else:
        #get the basic stats such as the players, current PB, the date, the rank, and the track score
        pb = get_player_current_pb(player_in, all_histories, track)
        date = get_player_current_pb_date(player_in, all_histories, track)
        standard = get_player_current_standard(player_in, all_histories, track)
        score = get_player_track_score(player_in, all_histories, track)
        placement = get_placements(all_histories,player_in,track)

        pb_history = get_player_line_graph(player_in, all_histories, track, extra_txt='nsc')

        output_string = f"{player_in}'s stats for {track} - NSC\n"
        output_string += f'Current PB: {pb} \n'
        output_string += f'Leaderboard Position: {placement} \n'
        output_string += f'Current Standard: {standard} \n'
        output_string += f'Date Set: {date} \n'
        output_string += f'Kartnite Score: {score} \n'
        await ctx.send(output_string)

        #include the record timeline
        file = discord.File(pb_history, filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send(f"{player_in}'s NSC Personal Best Timeline", file=file, embed=embed)

    await increment_stats(ctx.author.id)
    return 0


    

@bot.command()
async def tt_track_records(ctx, track = None):
    """Expects an argument <track>, returns the Kartnite Records"""

    if track not in TIME_TRIAL_TRACKS and track not in TT_TRACK_NICKNAME_LIST.keys():
        await ctx.send('Please Provide a valid track')
        return -1
    #if nickname replace
    if track in TT_TRACK_NICKNAME_LIST.keys():
        track = TT_TRACK_NICKNAME_LIST[track]

    #calculate all the history information
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}
    all_histories_nsc = {}

    #data is now in the format of: 
    #{player : {track: (time, date_set), ...}, ...}
    for player in players:
        all_histories[player] = convert_history_to_dict(player)
        all_histories_nsc[player] = convert_nsc_history_to_dict(player)

    #have different behaviors if the tracks have a shortcut.
    filepath_sc = None
    if track in TIME_TRIAL_SHORTCUT_TRACKS:
        filepath_sc = get_record_line(all_histories, track, extra_txt='sc')
        filepath_nsc = get_record_line(all_histories_nsc, track, extra_txt='nsc') 
    else:
        filepath_nsc = get_record_line(all_histories, track, extra_txt='nsc') 

    #send the nsc stats    
    file = discord.File(filepath_nsc, filename="image.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://image.png")
    await ctx.send("Kartnite NSC Record", file=file, embed=embed)

    #send the shortcut too if applicable
    if filepath_sc:
        file = discord.File(filepath_sc, filename="image.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://image.png")
        await ctx.send("Kartnite SC Record", file=file, embed=embed)

    await increment_stats(ctx.author.id)
    return 0
    



@bot.command()
async def tt_track_stats(ctx,track=None):
    """Expects an argument <track>, provides current TT leaderboards""" 

    if track not in TIME_TRIAL_TRACKS and track not in TT_TRACK_NICKNAME_LIST.keys():
        await ctx.send('Please Provide a valid track')
        return -1
    #if nickname replace
    if track in TT_TRACK_NICKNAME_LIST.keys():
        track = TT_TRACK_NICKNAME_LIST[track]

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

        sc_scores = get_time_trial_scores(all_histories, track)
        nsc_scores = get_time_trial_scores(all_histories_nsc, track)

        output_str = f'Non-Shortcut Leaderboard for {track}\n'
        output_str += non_shortcut.to_markdown(index=False) + "\n\n"

        output_str += f'NSC Kartnite Score for {track}\n'
        output_str += nsc_scores.to_markdown(index=False) + "\n\n"
        

        output_str += f'Shortcut Leaderboard for {track}\n'
        output_str += shortcut.to_markdown(index=False) + "\n\n"

        output_str += f'SC Kartnite Score for {track}\n'
        output_str += sc_scores.to_markdown(index=False) + "\n\n"

        await ctx.send(output_str)

    else:
        #when a track doesnt have a shortcut, use the open leaderboards...
        non_shortcut = get_current_leaderboard(all_histories, track, category='open')
        nsc_scores = get_time_trial_scores(all_histories, track)
        output_str = f'Non-Shortcut Leaderboard for {track}\n'
        output_str += non_shortcut.to_markdown(index=False) + "\n\n"
        output_str += f'NSC Kartnite Score for {track}\n'
        output_str += nsc_scores.to_markdown(index=False) + "\n\n"
        await ctx.send(output_str)
    
    await increment_stats(ctx.author.id)
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

    await increment_stats(ctx.author.id)
    return 0

# Run the bot with the token
bot.run(TOKEN)