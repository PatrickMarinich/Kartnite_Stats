#!/bin/bash

#The goal of this script is to allow the stats to be remotly updated using github

#THE IDEA
# 1. We play some races and I write down the results in my phone
# 2. I use github mobile to update the 'current_inputs.txt' with the data
# 3. Pull the repo
# 4. If there is something in that file, then run the script to input the data
# 5. If there was something in that file, then send out the player reports.



#attempt to pull the git repository
echo `git pull`;

#check if the file is empty, if not then run the stuff
if [ -s './recent_inputs/current_inputs.txt' ]; 
then
    echo 'Running Input Script';

    #runs the program to input the stats
    echo `python3 input/input_stats_remote.py`;


    #now that the stats are inputted, then push the updated stats
    echo `git add stats_csv/seasonal_stats`;
    echo `git commit -m 'Remote Stats Update' `;
    echo `git push`;

    echo 'done with updates!'

    #now send out the stats to the core players
    echo `python3 player_profile/remote_send_player_profiles_on_update.py Pat`
    echo `python3 player_profile/remote_send_player_profiles_on_update.py Demitri`
    echo `python3 player_profile/remote_send_player_profiles_on_update.py Kevin`
    echo `python3 player_profile/remote_send_player_profiles_on_update.py Chris`

    echo 'all stats sent out!'

else
    echo 'Not Running, No new data';
    echo 'Exiting...';
fi