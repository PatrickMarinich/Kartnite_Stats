#Patrick Marinich
#October 2024

#This is the script which will take the races inputted into the current_inputs.txt, parse the data, and update the csvs with the new infromation. 
#RUN THIS IF THERE IS NEW RACES LOCATED IN CURRENT_INPUTS.txt OTHERWISE THERE IS NO NEED TO RUN THIS (and it will do nothing *hopefully*)

import math
import random
import pandas as pd

#--------KVR HELPERS-----------

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


#---------Input Functions ----------

def inputRace(currentData,RaceCount,dfKartScore, dfPlacement,dfKVR, Track, Racers, Scores,TrackIndex):
  #checks to see if the track exists
  if Track in set(currentData["Tracks x Players"]):
    #print('Valid', Track)
    #seperates the players into an array, make sure that all players also exist

    racersArray = Racers.split()
    # checks that all players are valid
    validCount = 0
    for racer in racersArray:
      if(racer in set(currentData.columns.values.tolist())):
          #print('Valid', racer)
          validCount = validCount + 1
      else:
          validCount = validCount - 1
          print('Invalid', racer)


    if validCount == len(racersArray):
      #print("....Everything is valid, Updating the scores....")

      ##if all players are valid update the scores

      #gets scores into an array
      if Scores == 'q':
          newScores = [15,12,10,8]
      else:
        newScores = Scores.split()
      #changes to integers
      for i in range(len(newScores)):
        newScores[i] = int(newScores[i])
      #Adds new Score to the current score for each racer, uses the track index to find the track

      #calculate the track owner ahead of time, fixes edge case
      track_owners = getTrackOwner(currentData,RaceCount, Track, TrackIndex)
      for i in range(len(racersArray)):

        #only gives the points if there is a singular MVP
        if(len(track_owners.split()) == 1):
        #gives the track owner a tally for each person that played the track
          dfKartScore.at[0, track_owners] = int(dfKartScore.at[0, track_owners]) + 1


        #if the score is then 15, 12, 10, or 8, then increment the placement stats
        FIRSTPLACE_ROW = 0
        TOP2_ROW = 1
        TOP3_ROW = 2
        TOP4_ROW = 3
        #adds to the row if that place or higher was achieved, this is for percentage stats later!
        if newScores[i] == 15:
          dfPlacement.at[FIRSTPLACE_ROW,racersArray[i]] =  int(dfPlacement.at[FIRSTPLACE_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP2_ROW,racersArray[i]] =  int(dfPlacement.at[TOP2_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 12:
          dfPlacement.at[TOP2_ROW,racersArray[i]] =  int(dfPlacement.at[TOP2_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 10:
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 8:
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1

        #increments the score
        currentData.at[TrackIndex[Track],racersArray[i]] =  int(currentData.at[TrackIndex[Track],racersArray[i]]) + newScores[i]
        #increments the count
        RaceCount.at[TrackIndex[Track],racersArray[i]] =  int(RaceCount.at[TrackIndex[Track],racersArray[i]]) + 1
        #---------------end of loop--------

      #where KVR elements are stored
      CURRKVR = 0

      #compute the new KVRs for the players
      player1KVR = round(float(dfKVR.at[CURRKVR,racersArray[0]]))
      player2KVR = round(float(dfKVR.at[CURRKVR,racersArray[1]]))
      player3KVR = round(float(dfKVR.at[CURRKVR,racersArray[2]]))
      KVRarray = [player1KVR,player2KVR,player3KVR]
      if len(racersArray) == 4:
        player4KVR = round(float(dfKVR.at[CURRKVR,racersArray[3]]))
        KVRarray.append(player4KVR)

      #get the random values for the coms
      while len(KVRarray) != 12:
        KVRarray.append(random.randint(4750,5250))



      #now the array is 12 racers long, compute the expected points for each of the players

      expectedPlacements = getPlacementExpected(getEVArr(KVRarray))
      expectedPoints = []
      for item in expectedPlacements:
        expectedPoints.append(pointsExpected(item))

      #expected points has all of the values for the players and cpus that they SHOULD get
      #index 0 is player 1, ... , index 3 is player 4

      #get their new KVRs
      player1New = getNewKVR(player1KVR,expectedPoints[0],newScores[0])
      player2New = getNewKVR(player2KVR,expectedPoints[1],newScores[1])
      player3New = getNewKVR(player3KVR,expectedPoints[2],newScores[2])
      newKVRs = [player1New,player2New,player3New]
      if len(racersArray) == 4:
        player4New = getNewKVR(player4KVR,expectedPoints[3],newScores[3])
        newKVRs.append(player4New)

      #update the data frame,
      HISTORYSTART = 2
      HISTORYEND = 51

      #outer loop is j inner loop is i, sorry i know it is backwards, but
      # it is what it is!
      for j in range(len(racersArray)):
        #load history 49->50
        #load history 48->49
        #all the way until load 1->2
        for i in range (HISTORYEND,HISTORYSTART-1,-1):
          dfKVR.at[i,racersArray[j]] = round(float(dfKVR.at[i-1,racersArray[j]]))

        #load current into the first box in the history
        dfKVR.at[2,racersArray[j]] = dfKVR.at[0,racersArray[j]]

        #put the current KVR in the first box
        dfKVR.at[0,racersArray[j]] = round(newKVRs[j])

        #if this is a new all time max KVR, update it
        if newKVRs[j] > round(float(dfKVR.at[1,racersArray[j]])):
          dfKVR.at[1,racersArray[j]] = round(newKVRs[j])

    else:
      print('There was an error entering the racers, please try again')
  else:
    print('There was an error entering the track name, please try again:', Track, "was invalid")



def editAScore(dfScores, Track, Racer, Score,TrackIndex):
 #makes sure track is valid
  if Track in set(dfScores["Tracks x Players"]):
    print('Valid', Track)
    # makes sure racer is valid
    if Racer in set(dfScores.columns.values.tolist()):
      print('Valid', Racer)
      #changes a specific score
      dfScores.at[TrackIndex[Track],Racer] =  int(dfScores.at[TrackIndex[Track],Racer]) + int(Score)
      print(Racer, '\'s Score was changed by ', Score, ' on ', Track)
    else:
      print('There was an error entering the racer, please try again')
  else:
     print('There was an error entering the track name, please try again:', Track, "was invalid")

#allows for GP winners to be counted
def enterWinner(dfWins, Player):

  if Player in set(dfWins.columns.values.tolist()):

    dfWins.at[0, Player] = int(dfWins.at[0,Player]) + 1
    #print(Player, 'has', dfWins.at[0,Player], 'wins')


  else:
    print(Player, "does not exist within the Database, Please try again")

#allowes for Shock dodges
def enterDodges(dfShock, Player, Count):
  if Player in set(dfShock.columns.values.tolist()):

    dfShock.at[0, Player] = int(dfShock.at[0,Player]) + int(Count)
    #print(Player, 'has', dfShock.at[0,Player], 'shock dodges')


  else:
    print(Player, "does not exist within the Database, Please try again")

def addBlueShells(dfBlue, Player, hit, dodge):
  if Player in set(dfBlue.columns.values.tolist()):

    dfBlue.at[0, Player] = int(dfBlue.at[0,Player]) + int(hit)
    #print(Player, 'has been hit by', dfBlue.at[0,Player], 'Blue Shells')
    dfBlue.at[1, Player] = int(dfBlue.at[1,Player]) + int(dodge)
    #print(Player, 'has', dfBlue.at[1,Player], 'Blue Shell Dodges')

  else:
    print(Player, "does not exist within the Database, Please try again")


#----------------------- Stat Getters ------------------------
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

def getTrackOwner(dfScores,dfRaceCount, Track, TrackIndex):

  AVERAGE_PERCENT = .98
  TOTAL_PERCENT = .02

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
      playerScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) * TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT

      if playerScore > currentMaxScore:
        currentPlayer = player
        currentMaxScore = playerScore
      elif playerScore == currentMaxScore:
        currentPlayer = currentPlayer + ", " + player
      else:
        continue

  return currentPlayer

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




#Dictionaries needed here
PLAYERS_INIT = {
        "P":"Pat",
        "D":"Demitri",
        "K":"Kevin",
        "C":"Chris",
        "J":"Joe",
        "S":"Shane",
        "M":"Mike",
        "MA":"Matt",
        "JA":"Jason",
        "KA":"Karla",
        "CA":"Callum",
        "JW":"John",
        "DA":"Danny",
}
TrackIndex = {"Luigi Circuit":0,
    "Moo Moo Meadows":1,
    "Mushroom Gorge":2,
    "Toad's Factory":3,
    "Mario Circuit":4,
    "Coconut Mall":5,
    "DK Summit":6,
    "Wario's Gold Mine":7,
    "Daisy Circuit":8,
    "Koopa Cape":9,
    "Maple Treeway":10,
    "Grumble Volcano":11,
    "Dry Dry Ruins":12,
    "Moonview Highway":13,
    "Bowser's Castle":14,
    "Rainbow Road":15,
    "GCN Peach Beach":16,
    "DS Yoshi Falls":17,
    "SNES Ghost Valley 2":18,
    "N64 Mario Raceway":19,
    "N64 Sherbet Land":20,
    "GBA Shy Guy Beach":21,
    "DS Delfino Square":22,
    "GCN Waluigi Stadium":23,
    "DS Desert Hills":24,
    "GBA Bowser's Castle 3":25,
    "N64 DK's Jungle Parkway":26,
    "GCN Mario Circuit":27,
    "SNES Mario Circuit 3":28,
    "DS Peach Gardens":29,
    "GCN DK Mountain":30,
    "N64 Bowser's Castle":31,
    "Lava Lake":32,
    "Stargaze Summit":33,
    "Envenom Snowstorm":34,
    "Dragon Burial Grounds":35,
    "Bowser Jr.'s Crafty Castle":36,
    "N64 Royal Raceway":37,
    "DS Airstrip Fortress":38,
    "DK Ruins":39,
    "DS Bowser's Castle":40,
    "Wolf Castlegrounds":41
    }
NickNameIndex = {"Luigi":"Luigi Circuit",
    "LC":"Luigi Circuit",
    "moo moo": "Moo Moo Meadows",
    "Moo Moo": "Moo Moo Meadows",
    "MMM": "Moo Moo Meadows",
    "Gorge":"Mushroom Gorge",
    "gorge":"Mushroom Gorge",
    "MG":"Mushroom Gorge",
    "toads":"Toad's Factory",
    "Toads":"Toad's Factory",
    "TF":"Toad's Factory",
    "toads factory": "Toad's Factory",
    "mario circuit": "Mario Circuit",
    "MC": "Mario Circuit",
    "coconut mall":"Coconut Mall",
    "coconut":"Coconut Mall",
    "CM":"Coconut Mall",
    "summit":"DK Summit",
    "Summit":"DK Summit",
    "DKS":"DK Summit",
    "gold mine":"Wario's Gold Mine",
    "Gold Mine":"Wario's Gold Mine",
    "WGM":"Wario's Gold Mine",
    "DC" : "Daisy Circuit",
    "koopa": "Koopa Cape",
    "Koopa": "Koopa Cape",
    "KC": "Koopa Cape",
    "maple":"Maple Treeway",
    "Maple":"Maple Treeway",
    "MT":"Maple Treeway",
    "grumble":"Grumble Volcano",
    "Grumble":"Grumble Volcano",
    "GV":"Grumble Volcano",
    "Dry Dry":"Dry Dry Ruins",
    "dry dry":"Dry Dry Ruins",
    "DDR":"Dry Dry Ruins",
    "Moonview":"Moonview Highway",
    "moonview":"Moonview Highway",
    "MH":"Moonview Highway",
    "BC Wii":"Bowser's Castle",
    "bc wii":"Bowser's Castle",
    "BC wii":"Bowser's Castle",
    "BCWII":"Bowser's Castle",
    "BCWii":"Bowser's Castle",
    "BCW":"Bowser's Castle",
    "rainbow road":"Rainbow Road",
    "rainbow":"Rainbow Road",
    "Rainbow":"Rainbow Road",
    "RR":"Rainbow Road",
    "Peach Beach":"GCN Peach Beach",
    "peach beach":"GCN Peach Beach",
    "PB":"GCN Peach Beach",
    "yoshi falls":"DS Yoshi Falls",
    "Yoshi Falls":"DS Yoshi Falls",
    "YF":"DS Yoshi Falls",
    "Ghost Valley":"SNES Ghost Valley 2",
    "ghost valley":"SNES Ghost Valley 2",
    "GV2":"SNES Ghost Valley 2",
    "mario raceway":"N64 Mario Raceway",
    "raceway": "N64 Mario Raceway",
    "Raceway": "N64 Mario Raceway",
    "MR":"N64 Mario Raceway",
    "Sherbet Land":"N64 Sherbet Land",
    "sherbet land":"N64 Sherbet Land",
    "SL":"N64 Sherbet Land",
    "Shy Guy Beach":"GBA Shy Guy Beach",
    "shy guy beach":"GBA Shy Guy Beach",
    "Shy Guy":"GBA Shy Guy Beach",
    "shy guy":"GBA Shy Guy Beach",
    "SGB":"GBA Shy Guy Beach",
    "Delfino Square":"DS Delfino Square",
    "delfino square":"DS Delfino Square",
    "Delfino":"DS Delfino Square",
    "delfino":"DS Delfino Square",
    "DS":"DS Delfino Square",
    "Waluigi Stadium":"GCN Waluigi Stadium",
    "waluigi stadium":"GCN Waluigi Stadium",
    "WS":"GCN Waluigi Stadium",
    "Waluigi":"GCN Waluigi Stadium",
    "waluigi":"GCN Waluigi Stadium",
    "Desert Hills":"DS Desert Hills",
    "desert hills":"DS Desert Hills",
    "DH":"DS Desert Hills",
    "GBA 3":"GBA Bowser's Castle 3",
    "gba 3":"GBA Bowser's Castle 3",
    "BC3":"GBA Bowser's Castle 3",
    "bc3":"GBA Bowser's Castle 3",
    "Parkway":"N64 DK's Jungle Parkway",
    "parkway":"N64 DK's Jungle Parkway",
    "DKJP":"N64 DK's Jungle Parkway",
    "GCN mario circuit":"GCN Mario Circuit",
    "GCN mario":"GCN Mario Circuit",
    "gcn mario":"GCN Mario Circuit",
    "GCN Mario":"GCN Mario Circuit",
    "GCNMC":"GCN Mario Circuit",
    "SNES 3":"SNES Mario Circuit 3",
    "SNES3":"SNES Mario Circuit 3",
    "MC3":"SNES Mario Circuit 3",
    "snes 3":"SNES Mario Circuit 3",
    "Peach Gardens":"DS Peach Gardens",
    "peach gardens":"DS Peach Gardens",
    "PG":"DS Peach Gardens",
    "DK Mountain": "GCN DK Mountain",
    "DKM": "GCN DK Mountain",
    "dk mountain": "GCN DK Mountain",
    "mountain": "GCN DK Mountain",
    "Mountain": "GCN DK Mountain",
    "BC64":"N64 Bowser's Castle",
    "BCR":"N64 Bowser's Castle",
    "bc64":"N64 Bowser's Castle",
    "bc 64":"N64 Bowser's Castle",
    "N64BC":"N64 Bowser's Castle",
    "n64bc":"N64 Bowser's Castle",
    "LL" : "Lava Lake",
    "SS": "Stargaze Summit",
    "ES" : "Envenom Snowstorm",
    "DBG": "Dragon Burial Grounds",
    "BJCC": "Bowser Jr.'s Crafty Castle",
    "N64RR" : "N64 Royal Raceway",
    "AF": "DS Airstrip Fortress",
    "DKR": "DK Ruins",
    "BCDS" : "DS Bowser's Castle",
    "WC" : "Wolf Castlegrounds"}





import auto_parser as parser
import datetime as time
import os

#code for running main
if __name__ == "__main__":
    #constants
    VERSION_NUMBER = 'v3.3'
    CONTRIBUTORS = 'Patrick Marinich'
    print('Welcome to Kartnite Stats ' ,VERSION_NUMBER , "\nDeveloped by:", CONTRIBUTORS, '\n')
    #To start open all of the csvs that have the data in it, they will be overwritten during this process

    #seasonal Stats since those are what get updated during races
    dfScores = pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Total Scores.csv")
    dfRaceCount =  pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Race Count.csv")
    dfKartScore =  pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Owned Score.csv")
    dfPlacement =  pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Placement Stats.csv")
    dfKVR =  pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - KVR Stats.csv")
    dfWins = pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - GP Wins.csv")
    dfShock = pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Shock Dodges.csv")
    dfBlueShell = pd.read_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Blue Shells.csv")

    #parse the desired input file
    f = open('../recent_inputs/current_inputs.txt','r')
    data,error,info = parser.parse_input(f)

    if data == []:
       print("THERE WAS NO DATA TO PARSE!!")
       exit()

    #if there is ANYTHING in errors then quit
    if error != []:
        print("THERE EXISTS ERRORS DO NOT CONTINUE")
        for elem in error:
            print(elem)
        exit()
    
    #there are no errors so we can input the data
    #store the results in a new file so that the infromation can be saved...
    curr_time = str(time.datetime.now()).replace(" ","_").replace(".","_").replace(":",'_').replace("-","_")
    out_file = open('../recent_inputs/stats_from_' + curr_time + '.txt','w')
    
    #print(dfScores)
    for d in data:
        #write to the output file
        out_file.write(str(d)+'\n')
        #check what the current data contains, switch off of that
       
        #blueshell   (BLUE,COUNT,PLAYER)
        if d[0] == "BLUE" or d[0] == "DODGE":
            
            if d[0] == "BLUE":
                addBlueShells(dfBlueShell, d[2].capitalize(), int(d[1]), 0)
            else:
                addBlueShells(dfBlueShell, d[2].capitalize(), 0, int(d[1]))
               
        #shock (SHOCK,COUNT,PLAYER)
        elif d[0] == 'SHOCK':
            enterDodges(dfShock,d[2].capitalize(),int(d[1]))

        #gp wins ("WIN",player,score)
        elif d[0] == "GPWIN":
            enterWinner(dfWins, d[1].capitalize())
            #do something with score idk what yet since there is no deliberation between 3 and 4 players as of now

        #its a race
        else:
           
            # track is from nicknames
            # build racers string
            # build scores  string
            track = ""
            players = ""
            scores = ""
            for i in range(0,len(d)):
                if i == 0:
                   track = NickNameIndex[d[i]]
                else:
                    if i % 2 == 1:
                        players += PLAYERS_INIT[d[i]] + " "
                    else:
                        scores += str(d[i]) + " "

            #print(track, players, scores)
            inputRace(dfScores,dfRaceCount, dfKartScore, dfPlacement, dfKVR,track,players,scores,TrackIndex)

    #print(dfScores)
    print("Success! All Stats Entered....")
    print("Saving Entires.....")

    #save everything to csv
    dfScores.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Total Scores.csv",index=False)
    dfRaceCount.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Race Count.csv",index=False)
    dfKartScore.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Owned Score.csv",index=False)
    dfPlacement.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Placement Stats.csv",index=False)
    dfKVR.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - KVR Stats.csv",index=False)
    dfWins.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - GP Wins.csv",index=False)
    dfShock.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Shock Dodges.csv",index=False)
    dfBlueShell.to_csv("../stats_csv/seasonal_stats/Seasonal Kartnite Stats - Blue Shells.csv",index=False)


    print("Clearing current_inputs.txt")

    #erase the old file
    out_file.close()
    erase = open('../recent_inputs/current_inputs.txt','w')
    erase.close()
    print('Done!')


   