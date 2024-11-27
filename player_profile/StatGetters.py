import pandas as pd
from Constants import *
from copy import deepcopy
#This file will contain all of the methods that get different stats
#this will include all track stat getters, player stat getters, and seasonal and all time stat getters
#All of these stats are calculated here, and they are called within the I/O file or the Player Profile if nessassary

#This function gets all of the data for a specific track, includes things such as total race count,
#and a track ownership leaderboard
def GetTrackData(dfScores,dfRaceCount,Track,TrackIndex):
 
  AVERAGE_PERCENT = .96
  TOTAL_PERCENT = .04

  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
 
  #make sure that the track exists in the data
  if Track in set(dfScores["Tracks x Players"]):
    print("Stats For: ", Track)
    #now display the data for the track plus any interesting stats
    print("\n", "Total Scores")
    print(dfScores.loc[[TrackIndex[Track]]])

    races = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      races = races + int(dfRaceCount.at[TrackIndex[Track], player])
    print('\nTimes Played:',races )

    #prints player averages. 
    print('\nPlayer Averages:')
    for racer in set(dfNoTracks.columns.values.tolist()):
      print(racer,": ", getPlayerAverage(dfScores,dfRaceCount,racer,Track,TrackIndex))
    print('\n')
    print(getTrackOwner(dfScores, dfRaceCount, Track, TrackIndex), "is the MVP for this track")
    
    print('\nMVP Leaderboard')
    #determine the score for each player within the data
    dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'MVP Points':[]})
    counter = 0
   
    #gets the ownership scores of each player for the track
    TrackTotalPoints = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])
    for player in set(dfNoTracks.columns.values.tolist()):
      ownershipScore = 0
      if TrackTotalPoints != 0:
        ownershipScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) *TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT

      #puts the score into the datafram
      dfLeaderboard.loc[counter] = [player, ownershipScore]
      counter = counter + 1
      playerScore = 0

    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['MVP Points', 'Player'],  ascending=[0, 1])
    print(dfLeaderboard)

  else:
    print('Track Selection Was Invalid')



#this gets the track MVP of any specific track.
#A mix between total score and average is used to prevent a player from goign 1/1 on a track and owning it the whole season
#we all can agree that something along the lines of 9/10 is better then 2/2
def getTrackOwner(dfScores,dfRaceCount, Track, TrackIndex):

  AVERAGE_PERCENT = .96
  TOTAL_PERCENT = .04

  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]


  #goes through all players and then find the max score

  currentMaxScore = 0
  currentPlayer = ""
  TrackTotalPoints = 0
  for player in set(dfNoTracks.columns.values.tolist()):
    TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])

  if TrackTotalPoints != 0:
    for player in set(dfNoTracks.columns.values.tolist()):
      #way to calculate track owner, total points + average
      playerScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) *TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT
  
      if playerScore > currentMaxScore:
        currentPlayer = player
        currentMaxScore = playerScore
      elif playerScore == currentMaxScore:
        currentPlayer = currentPlayer + ", " + player
      else:
        continue

  return currentPlayer


#This is for the track owner all time, it uses only average rather then
#a mix of point total and average,
#there is a race minimum
RACE_MINIMUM = 5

def getAllTimeTrackOwner(dfScores,dfRaceCount,Track,TrackIndex):
  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]


  #goes through all players and then find the max score

  currentMaxScore = 0
  currentPlayer = ""
  TrackTotalPoints = 0
  for player in set(dfNoTracks.columns.values.tolist()):
    TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])

  if TrackTotalPoints != 0:
    for player in set(dfNoTracks.columns.values.tolist()):
      #way to calculate track owner, total points + average
      playerScore =  getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex)
  
      if playerScore > currentMaxScore and int(dfRaceCount.at[TrackIndex[Track], player]) >= RACE_MINIMUM:
        currentPlayer = player
        currentMaxScore = playerScore
      elif playerScore == currentMaxScore and int(dfRaceCount.at[TrackIndex[Track], player]) >= RACE_MINIMUM:
        currentPlayer = currentPlayer + ", " + player
      else:
        continue

  if currentPlayer == "":
    currentPlayer = "N/A"

  return currentPlayer


#gets a list of all of the track owners of every single track that the stats are kept for

def getAllTrackOwners(dfScores,dfRaceCount,TrackIndex, display=True):
  #the list that will get all of the track mvps
  dfList = pd.DataFrame({'Track': [], 'Current MVP': []})

  counter = 0
  for track in TrackIndex:
    mvp = getTrackOwner(dfScores,dfRaceCount, track, TrackIndex)
    dfList.loc[counter] = [track,mvp]
    counter = counter + 1

  if (display == True):
    print(dfList)
  return dfList


#Gets a list of the all time track owners, this uses a play minimum and only track average
#this never resets as the seasons change.

def getAllTimeAllTrackOwners(dfScores,dfRaceCount,TrackIndex,display = True):
  #the list that will get all of the track mvps
  dfList = pd.DataFrame({'Track': [], 'Current MVP': []})

  counter = 0
  for track in TrackIndex:
    mvp = getAllTimeTrackOwner(dfScores,dfRaceCount, track, TrackIndex)
    dfList.loc[counter] = [track,mvp]
    counter = counter + 1

  if (display == True):
    print(dfList)
  return dfList


#Gets the given players average on any specific track

def getPlayerAverage(dfScores, dfRaceCount, Player, Track, TrackIndex):
  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
  
  if Player in set(dfNoTracks.columns.values.tolist()):
    #checks for divide by 0

    RaceCount = int(dfRaceCount.at[TrackIndex[Track],Player])
    Score =  int(dfScores.at[TrackIndex[Track],Player])
   
    if(Score == 0 or RaceCount == 0):
      averageScore = 0
    else: 
      averageScore = Score/RaceCount
  
    

  else:
    averageScore = "ERROR"
    print("There was an internal with Averaging Have Pat re-read code")
  

  return averageScore


#-----------------------PLAYER SEEDING-------------------------------

def getPlayerStats(dfScores,dfRaceCount, dfWins,dfShock, dfKartScore, dfBlue, Player, TrackIndex):
  
  print("Displaying All Seasonal Stats for", Player)
  print("\n")
  print("---------------")
  #gets all of the tracks that the player owns
  Owns = ''
  for track in TrackIndex:
    if getTrackOwner(dfScores,dfRaceCount,track,TrackIndex) == Player:
      
      if Owns == '':
        Owns = track
      else:
        Owns = Owns + "\n" + track

  if(Owns == ''):
    print("Track MVP on: None")
  else:
    print("Tracks MVP on:\n", Owns)

  print("---------------")

  #prints total wins
  totalRaces = 0
  for Track in TrackIndex:
    totalRaces = totalRaces + int(dfRaceCount.at[TrackIndex[Track],Player])
  print("Total Races Played:", totalRaces)

  #Gp Wins
  print("Grand Prix Wins:", dfWins.at[0,Player])
  #dodges
  print("Shock Dodges:", dfShock.at[0,Player])
  #blue shell hits
  print("Times hit with a Blue:", dfBlue.at[0,Player])
  #blue shell dodges
  print("Blue Dodges:", dfBlue.at[1,Player])

  ####KART SCORE####
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
  KartScore = 0
  
  #gp wins points
  WinsScore = int(dfWins.at[0,Player])*GP_WINS_POINTS
    
  #owner score 
  OwnedScore = int(dfKartScore.at[0, Player]) * OWNER_POINTS
     
  #Dodges
  DodgeScore = int(dfShock.at[0,Player])*DODGE_POINTS
    
  #total points
  PointsScore = 0
  for track in TrackIndex:
   PointsScore = PointsScore + (int(dfScores.at[TrackIndex[track], Player])*POINTS_SCORED_POINTS)

  #adds in track averages
  avgScore = 0
  for track in TrackIndex:
    avgScore = avgScore + (int(getPlayerAverage(dfScores,dfRaceCount,Player,track,TrackIndex))*AVERAGE_POINTS)
  
  #points for blue shells
  blueScore = (int(dfBlue.at[0,Player]) * BLUE_POINTS) + (int(dfBlue.at[1,Player]) * BLUE_D_POINTS)



  KartScore = WinsScore + OwnedScore + DodgeScore + avgScore  + PointsScore + blueScore
  print('---------------')
  print("Kart Score:", KartScore)
  print('---------------')
  print("Kart Score Breakdown:")
  print('GP Win Points:', WinsScore)
  print('Points From Being Track MVP:', OwnedScore)
  print('Race Points:', PointsScore)
  print('Track Avg Points:', avgScore)
  print('Shock Dodge Points:', DodgeScore)
  print('Blue Shell Points:', blueScore)

  #prints the total Scores
  dfPlayerScores = dfScores[["Tracks x Players", Player]]
  print(Player, "\'s Total Scores")
  print("\n")
  print(dfPlayerScores)

  #prints Averages
  print("\n")
  print(Player, "\'s Track Averages")
  print("\n")
  for track in TrackIndex:
    print(track, "- ", getPlayerAverage(dfScores,dfRaceCount,Player,track,TrackIndex))

def getSeedings(dfKartScore,dfScores,dfRaceCount,dfWins,dfShock,dfBlue,TrackIndex,display=True):
    
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



#----------------ALL TIME PLAYER STATS-----------------


#This function will gather all of the stats for each player, all time.
#this is opposed to just the seasonal stats

#This function will get the data from the two different sheets and combine them into 
#a place where a given player can see all of their stats

#THIS FUNCTION IS DEPRECIATED, CURRENTLY UNUSED AND OUTDATED
def getAllTimeStats(season,allTime,player,TrackIndex):


    print('Loading Data....')
    #seasonal stats
    kartData = season.worksheet('Total Scores').get_all_values()
    RaceCount = season.worksheet('Race Count').get_all_values()
    Wins = season.worksheet('GP Wins').get_all_values()
    Shock = season.worksheet('Shock Dodges').get_all_values()
    OwnedScore = season.worksheet('Owned Score').get_all_values()
    Blue = season.worksheet('Blue Shells').get_all_values()
    
    #alltime stats
    kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
    RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
    WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
    ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()

    OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()

    BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
    SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
  

    print('Combining Old and New Data....')

    #the dataframes from each of the sheets (seasonal)
    dfSeasonOwnedScore = pd.DataFrame(OwnedScore[1:], columns = OwnedScore[0])
    dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfSeasonWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfSeasonShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    dfSeasonBlue = pd.DataFrame(Blue[1:], columns = Blue[0])

    #all time
    dfAllTimeOwnedScore = pd.DataFrame(OwnedScoreAllTime[1:], columns = OwnedScoreAllTime[0])
    dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
    dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])
    dfAllTimeWins = pd.DataFrame(WinsAllTime[1:], columns = WinsAllTime[0])
    dfAllTimeShock = pd.DataFrame(ShockAllTime[1:], columns = ShockAllTime[0])
    dfAllTimeBlue = pd.DataFrame(BlueAllTime[1:], columns = BlueAllTime[0])
    dfAllTimeSeeding = pd.DataFrame(SeedingAllTime[1:], columns =SeedingAllTime[0])


    print('Doing Calculations...')

    if player == 'all':
      dfAllTimeWins = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])]
      players = dfAllTimeWins.columns
    else:
      players = []
      players.append(player)


    for player in players:
    #combine the data frames into one df for use later in displaying the stats
      for track in TrackIndex:
        dfAllTimeScores.loc[TrackIndex[track], player] = int(dfAllTimeScores.at[TrackIndex[track], player]) + int(dfSeasonScores.at[TrackIndex[track], player])
        dfAllTimeRaceCount.loc[TrackIndex[track], player] = int(dfAllTimeRaceCount.at[TrackIndex[track], player]) + int(dfSeasonRaceCount.at[TrackIndex[track], player])
      
      #others not related to tracks
      dfAllTimeOwnedScore.loc[0,player] = float(dfAllTimeOwnedScore.loc[0,player]) + float(dfSeasonOwnedScore.loc[0,player])
      dfAllTimeWins.loc[0,player] = int(dfAllTimeWins.loc[0,player]) + int(dfSeasonWins.loc[0,player])
      dfAllTimeShock.loc[0,player] = int(dfAllTimeShock.loc[0,player]) + int(dfSeasonShock.loc[0,player])
    
      #blueshell is two columns
      dfAllTimeBlue.loc[0,player] = int(dfAllTimeBlue.loc[0,player]) + int(dfSeasonBlue.loc[0,player])
      dfAllTimeBlue.loc[1,player] = int(dfAllTimeBlue.loc[1,player]) + int(dfSeasonBlue.loc[1,player])
    

      #players total points scores, and races, tracks owned
      totalPoints = 0
      totalRaces = 0
      tracksOwned = 0
      for track in TrackIndex:
        totalPoints = totalPoints + int(dfAllTimeScores.loc[TrackIndex[track],player])
        totalRaces = totalRaces + int(dfAllTimeRaceCount.loc[TrackIndex[track],player])
        if (getAllTimeTrackOwner(dfAllTimeScores,dfAllTimeRaceCount,track,TrackIndex) == player):
          tracksOwned = tracksOwned + 1

        #fixes divide by 0 error
        if totalRaces == 0:
          average = 0
          FirstPlaceRate = 0
          avgGPScore= 0
          FirstPlaceEquivilent = 0

        else:
          average = totalPoints/totalRaces
          FirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (totalRaces/8))*100
          avgGPScore = (totalPoints) / (totalRaces/8)
          FirstPlaceEquivilent = totalPoints/15

    
        

        ##Display formatting and print statements
      print('\n\nDisplaying the All-Time Stats for', player)
      print('\n---Seeding Stats---')
      print('Normalized KartScore: ', dfAllTimeSeeding.at[0,player])
      print('All Time Kart Rating: ', getKartRating(dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,player,TrackIndex))
      
      print('\n---Race Stats---')
      print('Total Race Points: ', totalPoints)
      print('Total Race Count: ', totalRaces)
      print('Average Placement Points: ', average)
      print('First Place Equivalents: ', FirstPlaceEquivilent)
    
      print('\n---GP Stats---')
      print('Total GP Wins:', dfAllTimeWins.at[0,player])
      print('Total GPs Played:', totalRaces/8)
      print('GP First Place Rate: ', FirstPlaceRate , '%'  )
      print('Average GP Score: ', avgGPScore)

      print('\n---Misc Stats---')
      print('#1 Player on a Track: ', tracksOwned)
      print('Shock Dodges:', dfAllTimeShock.at[0,player])
      print('Times Hit By A Blue Shell:', dfAllTimeBlue.at[0,player])
      print('Blue Dodges: ', dfAllTimeBlue.at[1,player])
      print('Races Played on Owned Track', float(dfAllTimeOwnedScore.at[0,player])/4)
    


#Generates all of the leaderboards for the all time stats, it will display certin leaderboards if requested
#by the user
def getAllTimeLeaderboads(dfSeasonOwnedScore,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,
                          dfAllTimeOwnedScore,dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeSeeding,TrackIndex,display = True):
    #gets all of the data sheets opened, and then combines them into the all time 
   
    if display == True:
      print('Loading Data....')

    if display == True:
      print('Doing Calculations...')
    
    #make deep copies
    dfAllTimeScores_new = deepcopy(dfAllTimeScores)
    dfAllTimeRaceCount_new = deepcopy(dfAllTimeRaceCount)
    dfAllTimeOwnedScore_new = deepcopy(dfAllTimeOwnedScore)
    dfAllTimeWins_new = deepcopy(dfAllTimeWins)
    dfAllTimeShock_new = deepcopy(dfAllTimeShock)
    dfAllTimeBlue_new = deepcopy(dfAllTimeBlue)

    #gets a player list
    players = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])].columns
    #combines all of the data frames 
    for player in players:
    #combine the data frames into one df for use later in displaying the stats
      for track in TrackIndex:
        dfAllTimeScores_new.loc[TrackIndex[track], player] = int(dfAllTimeScores.at[TrackIndex[track], player]) + int(dfSeasonScores.at[TrackIndex[track], player])
        dfAllTimeRaceCount_new.loc[TrackIndex[track], player] = int(dfAllTimeRaceCount.at[TrackIndex[track], player]) + int(dfSeasonRaceCount.at[TrackIndex[track], player])
      
      #others not related to tracks
      dfAllTimeOwnedScore_new.loc[0,player] = float(dfAllTimeOwnedScore.loc[0,player]) + float(dfSeasonOwnedScore.loc[0,player])
      dfAllTimeWins_new.loc[0,player] = int(dfAllTimeWins.loc[0,player]) + int(dfSeasonWins.loc[0,player])
      dfAllTimeShock_new.loc[0,player] = int(dfAllTimeShock.loc[0,player]) + int(dfSeasonShock.loc[0,player])
    
      #blueshell is two columns
      dfAllTimeBlue_new.loc[0,player] = int(dfAllTimeBlue.loc[0,player]) + int(dfSeasonBlue.loc[0,player])
      dfAllTimeBlue_new.loc[1,player] = int(dfAllTimeBlue.loc[1,player]) + int(dfSeasonBlue.loc[1,player])


    #empty leaderboards for use below
    
    # -- Leaderboards for Power Points -- 
    dfPowerPointsLeaderboard = pd.DataFrame({'Player' : [], 'Seeding Power Points': []})
    dfNormalizedKartLeaderboard = pd.DataFrame({'Player': [], 'Kart Score' : []})
    dfKartRatingLeaderboard = pd.DataFrame({'Player' : [], 'Kart Rating': []})
    dfMiscRatingLeaderboard = pd.DataFrame({'Player' :  [], 'Misc Points' : []})

    #Other Leaderboards
    dfAllTimeAverageLeaderboard = pd.DataFrame({'Player': [], 'Average' : []})
    dfAllTimeWinsLeaderboard = pd.DataFrame({'Player' : [], 'GP Wins' : []})
    dfShockDodgesLeaderboard = pd.DataFrame({'Player' : [], 'Shock Dodges' : []})
    dfBlueShellsLeaderboard = pd.DataFrame({'Player' : [], 'Blue Shells Dodged': [], 'Blue Shells Hit' : []})
    dfRaceCountLeaderboard = pd.DataFrame({'Player' : [], 'Races Played': []})
    dfTotalPointsLeaderboard = pd.DataFrame({'Player' : [], 'Points Scored' : []})
    dfTracksOwnedLeaderboard = pd.DataFrame({'Player' : [], 'Tracks Owned' : []})

    #-----gets the current seasons normalized Kart scores ----------
    dfFinalRanks = getSeedings(dfSeasonOwnedScore,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,TrackIndex,display = False)
    SeasonalKartNormalizedScores = 0
    #get the total points,
    for index in dfFinalRanks.index:
      SeasonalKartNormalizedScores += dfFinalRanks.at[index,'Kart Score']
        #make a new leaderboard, and then add all the players to it with their new scores:
    dfSeasonScores = pd.DataFrame({'Player': [], 'Season Score':[]})
    for index in dfFinalRanks.index:
    #make score percent of score of the total:
      if SeasonalKartNormalizedScores != 0:
        score = (int(dfFinalRanks.at[index,'Kart Score']) / SeasonalKartNormalizedScores) * 100
      else:
        score = 0
      #multiplier for placements
      if(index == 0):
        score *= 1.25
      elif(index == 1):
        score *= 1.125
      elif(index == 2):
        score *= 1.05
      #print(dfSeasonScores)
      dfSeasonScores.loc[index] = [dfFinalRanks.at[index,'Player'],score]
      #dfSeasonScores.at[index,dfFinalRanks.at[index,'Player']] = score

    #generates all of the leaderboards
    currRow = 0
    for player in players:

      # ---- Calculations ---
      #players total points scores, and races, tracks owned
      totalPoints = 0
      totalRaces = 0
      tracksOwned = 0
      for track in TrackIndex:
        totalPoints = totalPoints + int(dfAllTimeScores_new.loc[TrackIndex[track],player])
        totalRaces = totalRaces + int(dfAllTimeRaceCount_new.loc[TrackIndex[track],player])
        if (getAllTimeTrackOwner(dfAllTimeScores_new,dfAllTimeRaceCount_new,track,TrackIndex) == player):
          tracksOwned = tracksOwned + 1

        #fixes divide by 0 error
        if totalRaces == 0:
          average = 0
          avgGPScore= 0
          miscScore = 0
        else:
          average = totalPoints/totalRaces
          FirstPlaceRate = (int(dfAllTimeWins_new.at[0,player]) / (totalRaces/8))*100
          avgGPScore = (totalPoints) / (totalRaces/8)
          FirstPlaceEquivilent = totalPoints/15
          miscScore = (int(dfAllTimeBlue_new.at[1,player])*BLUE_DODGE + int(dfAllTimeBlue_new.at[0,player])*BLUE_HIT + int(dfAllTimeShock_new.at[0,player])*SHOCK) / (totalRaces/8)
      

      #----LEADERBOARDS ---
      

      #---For Power Points---
      #print(dfSeasonScores)
      estimatedKartScore = float((dfSeasonScores.loc[dfSeasonScores['Player'] == player,'Season Score']).iloc[0]) + 0.85*float(dfAllTimeSeeding.at[0,player])
      
      #swapped all the .at to .loc
      dfNormalizedKartLeaderboard.loc[currRow] = [player, estimatedKartScore]
      rating = getKartRating(dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,player,TrackIndex)
      dfKartRatingLeaderboard.loc[currRow] = [player, rating]
      dfMiscRatingLeaderboard.loc[currRow] = [player, miscScore]

      # --- Other Leaderboards --
      dfAllTimeAverageLeaderboard.loc[currRow] = [player, average]
      dfAllTimeWinsLeaderboard.loc[currRow] = [player, dfAllTimeWins.at[0,player]]
      dfShockDodgesLeaderboard.loc[currRow] = [player, dfAllTimeShock.at[0,player]]
      dfBlueShellsLeaderboard.loc[currRow] = [player, dfAllTimeBlue.at[1,player], dfAllTimeBlue.at[0,player]]
      dfRaceCountLeaderboard.loc[currRow] = [player, totalRaces]
      dfTotalPointsLeaderboard.loc[currRow] = [player,totalPoints]
      dfTracksOwnedLeaderboard.loc[currRow] = [player,tracksOwned]

      #--loop --
      currRow = currRow + 1



    #-----SORT----
    dfNormalizedKart = dfNormalizedKartLeaderboard.sort_values(['Kart Score','Player'], ascending=[0,1])
    dfKartRating = dfKartRatingLeaderboard.sort_values(['Kart Rating', 'Player'],  ascending=[0, 1])
    dfAllTimeWins = dfAllTimeWinsLeaderboard.sort_values(['GP Wins', 'Player'], ascending=[0,1])
    dfAllTimeAverage = dfAllTimeAverageLeaderboard.sort_values(['Average', 'Player'], ascending=[0,1])
    dfAllTimeShockDodges = dfShockDodgesLeaderboard.sort_values(['Shock Dodges', 'Player'], ascending=[0,1])
    dfAllTimeBlueShells = dfBlueShellsLeaderboard.sort_values(['Blue Shells Dodged', 'Player'], ascending=[0,1])
    dfAllTimeRaceCount = dfRaceCountLeaderboard.sort_values(['Races Played', 'Player'], ascending=[0,1])
    dfAllTimeTotalPoints = dfTotalPointsLeaderboard.sort_values(['Points Scored', 'Player'], ascending=[0,1])
    dfAllTimeTracksOwned = dfTracksOwnedLeaderboard.sort_values(['Tracks Owned', 'Player'], ascending=[0,1]) 
    dfMiscScore = dfMiscRatingLeaderboard.sort_values(['Misc Points', 'Player'], ascending= [0,1])  


     #for the power points seeding leaderboard, matches player index to rank
    dfKartRankList = dfNormalizedKart['Kart Score'].rank(ascending = False)
    dfRatingRankList = dfKartRating['Kart Rating'].rank(ascending = False)
    dfMiscRankList = dfMiscScore['Misc Points'].rank(ascending = False)

    currRow = 0
    for player in players:
      #points for normalized kartscore, Rating, Misc Points.
      #index of the player
      PlayerIndex = dfNormalizedKart.index[dfNormalizedKart['Player']==player].tolist()
      #generate power points based on leaderboard positions
      kartPoints = (3 * len(dfNormalizedKart.index.values)) - (3*(int(dfKartRankList[PlayerIndex].iloc[0])))
      ratingPoints = (4 * len(dfKartRating.index.values)) - (4*(int(dfRatingRankList[PlayerIndex].iloc[0])))
      miscPoints = (1 * len(dfMiscScore.index.values)) - int(dfMiscRankList[PlayerIndex].iloc[0])
      #sum the points
      powerPoints = kartPoints + ratingPoints + miscPoints
      #add to list
      #was .at not .loc
      dfPowerPointsLeaderboard.loc[currRow] = [player,powerPoints]
      currRow = currRow + 1

    #sort Power Points to determine final all time seeding
    dfPowerPoints = dfPowerPointsLeaderboard.sort_values(['Seeding Power Points','Player'], ascending=[0,1])

    if display == True:
      print(dfPowerPoints)
      print('\n')
      print(dfNormalizedKart)
      print('\n')
      print(dfKartRating)
      print('\n')
      print(dfMiscScore)
      print('\n')
      print(dfAllTimeWins)
      print('\n')
      print(dfAllTimeAverage)
      print('\n')
      print(dfAllTimeShockDodges)
      print('\n')
      print(dfAllTimeBlueShells)
      print('\n')
      print(dfAllTimeRaceCount)
      print('\n')
      print(dfAllTimeTotalPoints)
      print('\n')
      print(dfAllTimeTracksOwned)
      print('\n')

    #--others--- 
    return dfPowerPoints,dfNormalizedKart,dfKartRating,dfMiscScore,dfAllTimeWins,dfAllTimeAverage,dfAllTimeShockDodges,dfAllTimeBlueShells,dfAllTimeRaceCount,dfAllTimeTotalPoints



#--------------------KART RATING----------------------
#this function returns the specific kart rating of a player
def getKartRating(dfScores,dfRaces,dfWins,player,TrackIndex):

  #gets total races and total points
  raceCount = 0
  totalPoints = 0
  for track in TrackIndex:
    raceCount = raceCount + int(dfRaces.at[TrackIndex[track], player])
    totalPoints = totalPoints + int(dfScores.at[TrackIndex[track], player])

  
  if raceCount == 0:
    gpWinPercentage = 0
    avgPointsPerGP = 0
  else:
    #assumes 8 race gps which is our standard and a max of 120 points
    gpWinPercentage = (int(dfWins.at[0,player]) / (raceCount / 8))
    #get the average points per GP
    avgPointsPerGP = totalPoints / (raceCount / 8)
    avgPointsPerGP = avgPointsPerGP / 120

  #gets the % of tracks owned
  count = 0
  for track in TrackIndex:
    output = getAllTimeTrackOwner(dfScores,dfRaces,track,TrackIndex)
    if output == player:
      count = count + 1

  tracksOwnedPercentage = count / len(TrackIndex)


  KartRating = (gpWinPercentage * POINTS_FOR_WINS) + (avgPointsPerGP * POINTS_FOR_AVERAGE) + (tracksOwnedPercentage * POINTS_FOR_TRACK)


  return KartRating


##creates a line plot of a players KVR history over the last 50 races 
import matplotlib.pyplot as plt
def make_line_plot(df, column):
    plt.clf()
    # Remove the first two rows
    df = df.iloc[2:]
    #make everything ints
    df = df.astype(int)
    #reverse the order so it is a history
    df = df.iloc[::-1].reset_index(drop=True)
    #create a line plot
   
    val = df[column].plot(x ="Race History",y = 'KVR', kind='line')
    plt.xlabel('Past 50 Races (0 = fifty races ago, 50 = most recent race)')
    plt.ylabel('KVR Value')
    name = 'KVRHistory.png'
    
  
    plt.savefig('KVRHistory.png')
  
    
    return name
   

  #---------ROMAN NUMERIAL CONVERTER FOUND ON STACK OVERFLOW-------
ROMAN = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
    (   4, "IV"),
    (   1, "I"),
  ]
def int_to_roman(number):
  result = ""
  for (arabic, roman) in ROMAN:
    (factor, number) = divmod(number, arabic)
    result += roman * factor
  return result



import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch

#Make Pie Charts for the GP win percentages of the season
def make_GP_pie_charts(dfS,dfA,player):

  #build arrays of info

  #get players list
  players = dfA[dfA.columns.difference(["Tracks x Players"])].columns
  
  seasonNames = []
  allNames = []
  seasonWins = []
  allWins = []
  for p in players:
    #they have won a GP at some point
    if int(dfA.at[0,p]) != 0:
      allNames.append(p)
      allWins.append(int(dfA.at[0,p]))
    #this season
    if int(dfS.at[0,p]) != 0:
      seasonNames.append(p)
      seasonWins.append(int(dfS.at[0,p]))

      
  #first generate the piechart for the season
  plt.clf()

  #formatting as percent (value)
  def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.3f}%\n({absolute:d})"

  fig = plt.figure(constrained_layout = True, figsize = (7,10))
  subplots = fig.subfigures(2,1)

  #make a subplot for the whole thing first
  ax0 = subplots[0].subplots(1,1)
  ax0.pie(seasonWins, labels = seasonNames, autopct=lambda pct: func(pct, seasonWins), radius = 1.2)
  ax0.set_title('GP Wins This Season')


  #all time, make the pie chart but explode it, using the example found in the matplotlib documentation
  #make the explode array based off the current player
  #subplot in the subplot
  ax1 = subplots[1].subplots(1,2)
  #s, (ax3,ax4) = plt.subplots(2,1, figsize = (3.5,5))
  explode = []
  cIndex = 0
  for i in range(len(allNames)):
    if allNames[i] == player:
      explode.append(0.1)
      cIndex = i
    else:
      explode.append(0)

  #print(explode)
  angle = -180 * allWins[0]
  wedges, *_ = ax1[0].pie(allWins, labels = allNames, autopct = lambda pct: func(pct, allWins), explode = explode,startangle = angle, radius = 1.1)
  ax1[0].set_title('GP Wins All-Time')

  #barchart
  #bar_labels =  ['Wins This Season', 'Out of Season Wins']
  #get the wins by previous seasons, then add the current season
  if player in PLAYER_GP_WINS_PAST_SEASONS.keys():
    bar_values = PLAYER_GP_WINS_PAST_SEASONS[player]
  else:
    bar_values = []
  bar_values.append(int(dfS.at[0,player]))
  bottom = 1
  width = .2
  
  #get the seasons names
  bar_labels = []
  for i in range(len(bar_values)):
    bar_labels.append("Season " + int_to_roman(i+1))

  #print(bar_values)
  #print(bar_labels)

  for j, (height, label) in enumerate(reversed([*zip(bar_values, bar_labels)])):
    bottom -= height
    bc = ax1[1].bar(0, height, width, bottom=bottom, label=label,
                 alpha=0.1 + (1/len(bar_values)) * j)
    ax1[1].bar_label(bc, labels=[f"{height:1.0f}"], label_type='center')

  ax1[1].set_title(player + '\'s GP Wins By Season')
  ax1[1].legend()
  ax1[1].axis('off')
  ax1[1].set_xlim(- 2.5 * width, 2.5 * width)

  #plt.show()
  #saves to a file to be used by the pdf maker
  plt.savefig('GPWins.png')
    

#These are the KVR Helper Stats
import math
import random

#using the expectation of a win formula I developed, calculate the odds that racer 1 beats racer 2
#returns a value between 0 and 1
def getExpectedWinRate(kvr1,kvr2):
  pointDiff = abs(kvr1-kvr2)
  expterm = 0.5 * (1 - math.exp((-.0004 * pointDiff)))
  if kvr1 > kvr2:
    return 0.5+expterm, 0.5-expterm
  else:
    return 0.5-expterm, 0.5+expterm


#given an array of 12 kvrs, return the expected win array
def getEVArr(arr):
  EVs = []
  for i in range(0,len(arr)):
    playerScore = 0
    for j in range(0,len(arr)):
        if i != j:
          ev1,ev2 = getExpectedWinRate(arr[i],arr[j])
          playerScore = playerScore + ev1
    EVs.append(playerScore)

  return EVs

#Evarr is the expect amount of wins, however placement is the reverse of wins, so convert
#ie. 12Wins -> first place or 2Wins -> tenth
def getPlacementExpected(arr):
  for i in range(0,len(arr)):
    arr[i] = 12 - arr[i]
  return arr

#given a place value, determine the amount of ingame points following the peicewise function below
def pointsExpected(placement):
  if(placement >=1 and placement <=2):
    points = (-3 * placement) + 18
  elif (placement > 2 and placement <= 4):
    points = (-2*placement) + 16
  else:
    points = (-1*placement) + 12
  return points


#gets the new KVR of the player given their current, expected points, and points scored
def getNewKVR(currKVR,ExPoints,actualPoints):
  return (currKVR + (20 * (actualPoints - ExPoints)))

#Gets all the need to know stats about every track that we play
def getTrackStats(dfScores,dfRaceCount,dfAllScores,dfAllRaceCount,Track,TrackIndex):
  
  #Calculating the current seasonal track owner
  AVERAGE_PERCENT = .96
  TOTAL_PERCENT = .04

  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
  
  #make sure that the track exists in the data
  if Track in set(dfScores["Tracks x Players"]):
    #print("Stats For: ", Track)
    #now display the data for the track plus any interesting stats
    #print("\n", "Total Scores")
    #print(dfScores.loc[[TrackIndex[Track]]])

    seasonRaces = 0
    allRaces = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      seasonRaces = seasonRaces + int(dfRaceCount.at[TrackIndex[Track], player])
      allRaces = allRaces + int(dfAllRaceCount.at[TrackIndex[Track],player])
    #print('\nTimes Played:',races )


    #prints player averages. 
    #print('\nPlayer Averages:')
    #for racer in set(dfNoTracks.columns.values.tolist()):
    #print(racer,": ", getPlayerAverage(dfScores,dfRaceCount,racer,Track,TrackIndex))
    #print('\n')
    #print(getTrackOwner(dfScores, dfRaceCount, Track, TrackIndex), "is the MVP for this track")
    
    #print('\nMVP Leaderboard')
    #determine the score for each player within the data
    dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfSeasonMVPLeaderboard = pd.DataFrame({'Player': [], 'Score':[]})
    dfAllMVPLeaderboard = pd.DataFrame({'Player': [], 'Score':[]})
    counter = 0
   
    #gets the ownership scores of each player for the track
    TrackTotalPoints = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])
    for player in set(dfNoTracks.columns.values.tolist()):
      ownershipScore = 0
      allOwnershipScore = 0
      if TrackTotalPoints != 0:
        ownershipScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) *TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT
      
      allOwnershipScore = round(getPlayerAverage(dfAllScores,dfAllRaceCount,player,Track,TrackIndex),2)
      #puts the score into the datafram
      dfSeasonMVPLeaderboard.loc[counter] = [player, round(ownershipScore,2)]
      dfAllMVPLeaderboard.loc[counter] = [player,allOwnershipScore]
      counter = counter + 1
      playerScore = 0

    #sorts and prints the leaderboards
    dfSeasonMVPLeaderboard = dfSeasonMVPLeaderboard.sort_values(['Score', 'Player'],  ascending=[0, 1])
    dfAllMVPLeaderboard = dfAllMVPLeaderboard.sort_values(['Score', 'Player'],  ascending=[0, 1])
    


    return seasonRaces/4,allRaces/4,dfSeasonMVPLeaderboard,dfAllMVPLeaderboard
  #bad track selection
  return 'ERROR'