# Kartnite_Stats

## General Info 
Version 4.0, automation work

Dec 2021 -> Current

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excel spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite Stats* was born. 

**Goal:** This scripts goal is to take user inputted *Mario Kart Wii* races and other stats and save them to be used for calculations and analysis when user requested. 

# Table of Contents
    - Documentation - Contains documentation about the various custom stats that are being used as well as the patch notes
    - input - These python files are what is used for inputting the data from our races
    - player_profile - These are the python files used to generate the player report pdf and email them out to the players. PNGs generated also are stored here
    - recent_inputs - Where the inputs are stored. Current_inputs.txt is the file read by the input functions to grab the data.
    - stats_csv - Where all of the csv files for the stats live, these are what store our data    
**Note**
Inside of the player_profile folder, there is a program file wkhtmltopdf.exe, which I did not create for converting html to pdf. (https://github.com/wkhtmltopdf/wkhtmltopdf) 

# Notes
All File paths are now relative to their respective locations witin the file tree, so if files are moved around these have to be changed. It also means that if you are running the 
code in vscode or another IDE, then the current directory must be set to where the main function lives so that file paths are correct.

# Contributions
## Pat
placeholder....