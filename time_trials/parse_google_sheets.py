#June 2025

# Time Trials are a different beast compared to our LAN playing events.
# In terms of the code, the main difference is that all players need the ability to remotely input their times for this to be a feasable
# system. Before this point we used a 'shared note' on the notes app to accomplish this. But now (june 2025) it is time to start a full effort
# into converting the notes app into something that can be presented in the known pdf fashion
#
# The plan: Use a shared google sheet, have my server pull the changes daily to look for updates, track all data and any updates
# Then compile a report which showcases the data in a nice fashion alongside the current stats PDF
#
# Some things that I am interested in doing
# Making a graph of all our times over time, to track the progress on all tracks
# Do something with the Standards list
# A checklist to see if we have beaten the staff ghosts.

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import pandas as pd
from datetime import datetime

PATH_EXT = "/home/pat/KartniteStats/Kartnite_Stats/"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1iTX_znc3otAyS15sWvM-fVH7wk8EAKdrtvQJ8C2ULuo"

#this function is responsible for grabbing the data from our google sheet
def get_player_sc_times(player):
  SAMPLE_RANGE_NAME = player+'!B3:G34'

  creds = service_account.Credentials.from_service_account_file(PATH_EXT+'time_trials/credentials.json')
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    tracks = []
    times = []
    dates = []
    for row in values:
      tracks.append(row[0])
      times.append(row[2])
      dates.append(row[5])
    
    data = {"Tracks":tracks, "Times":times,"Dates": dates}
    return pd.DataFrame(data)

  except HttpError as err:
    print(err)

#copy of the previous but for the nsc times -> currently not being used, but being tracked
def get_player_nsc_times(player):
  SAMPLE_RANGE_NAME = player+"nSC"+'!B3:G34'

  creds = service_account.Credentials.from_service_account_file(PATH_EXT+'time_trials/credentials.json')
  try:
    service = build("sheets", "v4", credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    tracks = []
    times = []
    dates = []
    for row in values:
      tracks.append(row[0])
      times.append(row[2])
      dates.append(row[5])
    
    data = {"Tracks":tracks, "Times":times,"Dates": dates}
    return pd.DataFrame(data)

  except HttpError as err:
    print(err)

#updates the player database if there are new times to report, otherwise nothing happens. The player database consists of the player history
#and their current times, for both shortcut and non-shortcut
def update_player_database(player):
    print("Checking "+player+" for updates")
    #get the current values from google sheets
    sc = get_player_sc_times(player)
    nsc = get_player_nsc_times(player)
  
    #open up the current values
    stored = pd.read_csv(PATH_EXT+"time_trials/player_data/shortcut/" + player + ".csv")
    stored_nsc = pd.read_csv(PATH_EXT+"time_trials/player_data/non_shortcut/" + player + ".csv")

    #compare the read to the stored. If there is a difference print it.
    format_str = "%M:%S.%f" 
    update_count = 0
    for i in range(len(sc)):
        row_read = sc.iloc[i]
        row_stored = stored.iloc[i]

        time1 = datetime.strptime(row_read.Times, format_str)
        time2 = datetime.strptime(row_stored.Times, format_str)

        history_file = open(PATH_EXT+"time_trials/player_data/shortcut/"+player+"_history.csv", "a")
        if (time1 < time2):
            update_count += 1
            print(player+ " decreased their time by: " + str(time2 - time1)[:-3] + " on " + row_read.Tracks + " Shortcut")
            #if we have a new best time, we want to write it to the history at the end... will be useful later
            history_file.write(str(row_read.Tracks+','+time1.strftime(format_str)[:-3]+','+row_read.Dates+'\n'))
        history_file.close()

    #overwrite the stored values with the read in values
    sc.to_csv(PATH_EXT+"time_trials/player_data/shortcut/"+player+".csv",index=False)
    
    #now repeat for the non-shortcut times
    for i in range(len(nsc)):
        row_read = nsc.iloc[i]
        row_stored = stored_nsc.iloc[i]

        time1 = datetime.strptime(row_read.Times, format_str)
        time2 = datetime.strptime(row_stored.Times, format_str)

        history_file = open(PATH_EXT+"time_trials/player_data/non_shortcut/"+player+"_history.csv", "a")
        if (time1 < time2):
            update_count += 1
            print(player+ " decreased their time by: " + str(time2 - time1)[:-3] + " on " + row_read.Tracks + " Non-Shortcut")
            #if we have a new best time, we want to write it to the history at the end... will be useful later
            history_file.write(str(row_read.Tracks+','+time1.strftime(format_str)[:-3]+','+row_read.Dates+'\n'))
        history_file.close()

    #overwrite the stored values with the read in values
    nsc.to_csv(PATH_EXT+"time_trials/player_data/non_shortcut/"+player+".csv",index=False)
    
    
    return update_count

  

if __name__ == "__main__":
    #for all players, update their player databases from the sheet
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    update_count = 0
    for player in players:
       print("Updating: " + player + "...")
       update_count = update_player_database(player)
       print(player+" had "+ str(update_count) +" new times!")
    print("All players successfully updated!")

  