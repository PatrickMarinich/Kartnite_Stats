#this is the code to be run when we want to start a new season. 
#this should only be run once the season is declared to be OVER.

#from pandas.core.dtypes.cast import sanitize_to_nanoseconds
from Constants import *
from LeaderboardGenerators import *
from PlayerProfile import *
from StatGetters import *

#from player_profile 
import pandas as pd

def getSeedings(dfScores,dfRaceCount,dfKartScore,dfPlacement,dfKVR,dfWins,dfShock,dfBlue,TrackIndex):

    
    #determine the score for each player within the data
    dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Kart Score':[]})
    counter = 0

    #sets up the scores for each player
    for player in set(dfNoTracks.columns.values.tolist()):
      playerScore = 0
      #gp wins
      playerScore = int(dfWins.at[0,player])*GP_WINS_POINTS

      #enters the owned track score
      playerScore = playerScore + int(dfKartScore.at[0, player])*OWNER_POINTS


      #Dodges
      playerScore = int(dfShock.at[0,player])*DODGE_POINTS + playerScore

      #total points
      points = 0
      for track in TrackIndex:
        points = points + int(dfScores.at[TrackIndex[track], player]) * POINTS_SCORED_POINTS
      playerScore = playerScore + points

      #adds in track averages
      avgpoints = 0
      for track in TrackIndex:
        avgpoints = avgpoints + (int(getPlayerAverage(dfScores,dfRaceCount,player,track,TrackIndex))*AVERAGE_POINTS)
      playerScore = playerScore + avgpoints
      avgpoints = 0
      #adds blue points
      playerScore = playerScore + (int(dfBlue.at[0,player]) * BLUE_POINTS) + (int(dfBlue.at[1,player]) * BLUE_D_POINTS)

      #puts the score into the datafram
      dfLeaderboard.loc[counter] = [player, playerScore]
      counter = counter + 1
      playerScore = 0

    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Kart Score', 'Player'],  ascending=[0, 1])

    if display == True:
      print(dfLeaderboard)

    return dfLeaderboard





#transfers all the data
def transfer_data(dfOldKart,dfNewKart):
  #deleats first column
  colList = dfOldKart.columns.values.tolist();
  del colList[0]

  #iterates through the sheets
  for col in colList:
    for row in dfOldKart.index:
        dfNewKart.at[row,col] = float(dfNewKart.at[row,col]) + float(dfOldKart.at[row,col])
        #clears the old stats
        dfOldKart.at[row,col] = 0

  return dfNewKart,dfOldKart;


#This function will take all of the seasonal stats that have been aquired,
#increment them into the all time sheet, and the reset the season for the next use
def end_season(TrackIndex):
  
    #seasonal Stats since those are what get updated during races
    dfScores = pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Total Scores.csv")
    dfRaceCount =  pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Race Count.csv")
    dfKartScore =  pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Owned Score.csv")
    dfPlacement =  pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Placement Stats.csv")
    dfKVR =  pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - KVR Stats.csv")
    dfWins = pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - GP Wins.csv")
    dfShock = pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Shock Dodges.csv")
    dfBlueShell = pd.read_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Blue Shells.csv")

    # #all time
    dfAllTimeOwnedScore =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Owned Score.csv')
    dfAllTimeScores =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Total Scores.csv')
    dfAllTimeRaceCount =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Race Count.csv')
    dfAllTimeWins =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - GP Wins.csv')
    dfAllTimeShock =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Shock Dodges.csv')
    dfAllTimeBlue =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Blue Shells.csv')
    dfAllTimeSeeding =  pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - All-Time Seeding.csv')
    dfAllTimePlacement = pd.read_csv('stats_csv/all_time/All-Time Kartnite Stats - Placement Stats.csv')

    #first get the seeding points and then update the kart sheet
    dfFinalRanks = getSeedings(dfScores,dfRaceCount,dfKartScore,dfPlacement,dfKVR,dfWins,dfShock,dfBlueShell,TrackIndex)

    #find the score of each player using the decided algorythem, and then
    #increment this score with the all time score

    totalScores = 0
    #get the total points,
    for index in dfFinalRanks.index:
        totalScores += dfFinalRanks.at[index,'Kart Score']


    #make a new leaderboard, and then add all the players to it with their new scores:
    dfSeasonScores = pd.DataFrame({'Player': [], 'Season Score':[]})
    for index in dfFinalRanks.index:
        #make score percent of score of the total:
        score = (int(dfFinalRanks.at[index,'Kart Score']) / totalScores) * 100
        #multiplier for placements
        if(index == 0):
            score *= 1.10
        elif(index == 1):
            score *= 1.06
        elif(index == 2):
            score *= 1.02

        #dfFinalRanks.at[index,'Player']
        dfSeasonScores.loc[index] = [dfFinalRanks.at[index,'Player'],score]

    print("Below are the Final Scores Normalized for the Season")
    print(dfSeasonScores)


    #adds the new df to the all time scoring sheet
    #do something here
    #all_timeScores= all_time.worksheet('All-Time Seeding').get_all_values()
    #dfAll_timeScores = pd.DataFrame(all_timeScores[1:], columns = all_timeScores[0])


    print('Updating All Time Seeding....')
    print('Diminishing Old Seasons by 15%...')
    print('Incrementing The New Seasons Scores...')

    for index in dfSeasonScores.index:
        player = dfSeasonScores.at[index,'Player']


        dfAllTimeSeeding.at[0,player] = (float(dfAllTimeSeeding.at[0,player])*.85) + float(dfSeasonScores.at[index,'Season Score'])

    #increments the all time stats with the seasonal stats, and then clears all of the seasonal stats

    #calls the transfer function on points score
    newPoints,oldPoints = transfer_data(dfScores,dfAllTimeScores)
    #calls it for the race count
    newRaceCount,oldRaceCount = transfer_data(dfRaceCount,dfAllTimeRaceCount)
    #GP Wins
    newWins,oldWins = transfer_data(dfWins,dfAllTimeWins)
    #Shock Dodges
    newDodge,oldDodge = transfer_data(dfShock,dfAllTimeShock)
    #races owned
    newOwned,oldOwned = transfer_data(dfKartScore,dfAllTimeOwnedScore)
    #blue Shells
    newShells,oldShells = transfer_data(dfBlueShell,dfAllTimeBlue)
    #placement stats
    newPlacement,oldPlacement = transfer_data(dfPlacement,dfAllTimePlacement)
    ##DO NOT TRANSFER KVR CODE


    return newPoints,newRaceCount,newWins,newDodge,newOwned,newShells,dfAllTimeSeeding,oldPoints,oldRaceCount,oldWins,oldDodge,oldOwned,oldShells,newPlacement,oldPlacement


if __name__ == '__main__':
  newPoints,newRaceCount,newWins,newDodge,newOwned,newShells,newSeeds,oldPoints,oldRaceCount,oldWins,oldDodge,oldOwned,oldShells,newPlacement,oldPlacement = end_season(TrackIndex)
  #make sure these values make sense
  print(oldShells)
  print(newShells)
        
  a = input("are you sure you would like to reset?")
  if a == 'yes':
    p = input("enter password")
    if p == 'resetseason123':
      #saving all csvs; to reset, uncomment all of these and run; commented out for saftey
      #oldPoints.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Total Scores.csv",index=False)
      #oldRaceCount.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Race Count.csv",index=False)
      #oldOwned.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Owned Score.csv",index=False)
      #oldPlacement.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Placement Stats.csv",index=False)
      #oldWins.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - GP Wins.csv",index=False)
      #oldDodge.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Shock Dodges.csv",index=False)
      #oldShells.to_csv("stats_csv/seasonal_stats/Seasonal Kartnite Stats - Blue Shells.csv",index=False)
      #newOwned.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Owned Score.csv',index=False)
      #newPoints.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Total Scores.csv',index=False)
      #newRaceCount.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Race Count.csv',index=False)
      #newWins.to_csv('stats_csv/all_time/All-Time Kartnite Stats - GP Wins.csv',index=False)
      #newDodge.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Shock Dodges.csv',index=False)
      #newShells.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Blue Shells.csv',index=False)
      #newSeeds.to_csv('stats_csv/all_time/All-Time Kartnite Stats - All-Time Seeding.csv',index=False)
      #newPlacement.to_csv('stats_csv/all_time/All-Time Kartnite Stats - Placement Stats.csv',index=False)

      print("A new season is upon us!!!")
    else:
      print("bad password")
  else:
    print("type yes")