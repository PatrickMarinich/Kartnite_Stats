from Constants import *
from LeaderboardGenerators import *
from StatGetters import * 

import time
import pdfkit
import yagmail
#import wkhtmltopdf

import sys
from IPython import display
import pdfkit
from datetime import date

#this file gets all of the leaderboards and generates a html player profile for any given player

#it will get all of the stats, generate html code, convert it to a pdf, and the email it out to the given player

#CHECK AROUND LINES 150-160 FOR THE PAGE ORDER,CODE FOR PAGE GENERATION IS BELOW THIS

#############################################

#this method generates all of the stats and wraps them in html tags and formatting

def createPlayerProfile(player,TrackIndex):
  #----OPENING THE DATA----
  print('Loading Data....')

  # #seasonal stats
  # kartData = season.worksheet('Total Scores').get_all_values()
  # RaceCount = season.worksheet('Race Count').get_all_values()
  # Wins = season.worksheet('GP Wins').get_all_values()
  # Shock = season.worksheet('Shock Dodges').get_all_values()
  # OwnedScore = season.worksheet('Owned Score').get_all_values()
  # Blue = season.worksheet('Blue Shells').get_all_values()
  # kvr = season.worksheet('KVR Stats').get_all_values()
  # placement = season.worksheet('Placement Stats').get_all_values()

  # print('Downloading Seasonal Data....')
  # time.sleep(30)

  # #alltime stats
  # kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
  # RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
  # WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
  # ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()

  # OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()

  # BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
  # SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
  # placementAllTime = allTime.worksheet('Placement Stats').get_all_values()
  
  # print('Downloading All-Time Data....')
  # time.sleep(30)

  # print('Analyzing Old and New Data....')

  # #the dataframes from each of the sheets (seasonal)
  # dfSeasonOwnedScore = pd.DataFrame(OwnedScore[1:], columns = OwnedScore[0])
  # dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
  # dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
  # dfSeasonWins = pd.DataFrame(Wins[1:], columns = Wins[0])
  # dfSeasonShock = pd.DataFrame(Shock[1:], columns = Shock[0])
  # dfSeasonBlue = pd.DataFrame(Blue[1:], columns = Blue[0])
  # dfKVR = pd.DataFrame(kvr[1:],columns = kvr[0])
  # dfSeasonPlacement = pd.DataFrame(placement[1:],columns = placement[0])

  # #all time
  # dfAllTimeOwnedScore = pd.DataFrame(OwnedScoreAllTime[1:], columns = OwnedScoreAllTime[0])
  # dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
  # dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])
  # dfAllTimeWins = pd.DataFrame(WinsAllTime[1:], columns = WinsAllTime[0])
  # dfAllTimeShock = pd.DataFrame(ShockAllTime[1:], columns = ShockAllTime[0])
  # dfAllTimeBlue = pd.DataFrame(BlueAllTime[1:], columns = BlueAllTime[0])
  #dfAllTimeSeeding = pd.DataFrame(SeedingAllTime[1:], columns =SeedingAllTime[0])
  # dfAllTimePlacement = pd.DataFrame(placementAllTime[1:],columns = placementAllTime[0])

  #rather than doin all that.... load in the csvs!!
  #seasonal
  dfSeasonOwnedScore = pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Owned Score.csv')
  dfSeasonScores =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Total Scores.csv')
  dfSeasonRaceCount =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Race Count.csv')
  dfSeasonWins =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - GP Wins.csv')
  dfSeasonShock =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Shock Dodges.csv')
  dfSeasonBlue =   pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Blue Shells.csv')
  dfKVR =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - KVR Stats.csv')
  dfSeasonPlacement =  pd.read_csv('..\\stats_csv\\seasonal_stats\\Seasonal Kartnite Stats - Placement Stats.csv')

  # #all time
  dfAllTimeOwnedScore =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Owned Score.csv')
  dfAllTimeScores =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Total Scores.csv')
  dfAllTimeRaceCount =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Race Count.csv')
  dfAllTimeWins =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - GP Wins.csv')
  dfAllTimeShock =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Shock Dodges.csv')
  dfAllTimeBlue =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Blue Shells.csv')
  dfAllTimeSeeding =  pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - All-Time Seeding.csv')
  dfAllTimePlacement = pd.read_csv('..\\stats_csv\\all_time\\All-Time Kartnite Stats - Placement Stats.csv')

  print('Doing Calculations...')
 
  dfAllTimeWins = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])]
  players = dfAllTimeWins.columns
 
  for racer in players:
  #combine the data frames into one df for use later in displaying the stats
    for track in TrackIndex:
      dfAllTimeScores.loc[TrackIndex[track], racer] = int(dfAllTimeScores.at[TrackIndex[track], racer]) + int(dfSeasonScores.at[TrackIndex[track], racer])
      dfAllTimeRaceCount.loc[TrackIndex[track], racer] = int(dfAllTimeRaceCount.at[TrackIndex[track], racer]) + int(dfSeasonRaceCount.at[TrackIndex[track], racer])
      
    #others not related to tracks
    dfAllTimeOwnedScore.loc[0,racer] = float(dfAllTimeOwnedScore.loc[0,racer]) + float(dfSeasonOwnedScore.loc[0,racer])
    dfAllTimeWins.loc[0,racer] = int(dfAllTimeWins.loc[0,racer]) + int(dfSeasonWins.loc[0,racer])
    dfAllTimeShock.loc[0,racer] = int(dfAllTimeShock.loc[0,racer]) + int(dfSeasonShock.loc[0,racer])
    
    #blueshell is two columns
    dfAllTimeBlue.loc[0,racer] = int(dfAllTimeBlue.loc[0,racer]) + int(dfSeasonBlue.loc[0,racer])
    dfAllTimeBlue.loc[1,racer] = int(dfAllTimeBlue.loc[1,racer]) + int(dfSeasonBlue.loc[1,racer])

    #placement is 4 rows
    dfAllTimePlacement.loc[0,racer] = int(dfAllTimePlacement.loc[0,racer]) + int(dfSeasonPlacement.loc[0,racer])
    dfAllTimePlacement.loc[1,racer] = int(dfAllTimePlacement.loc[1,racer]) + int(dfSeasonPlacement.loc[1,racer])
    dfAllTimePlacement.loc[2,racer] = int(dfAllTimePlacement.loc[2,racer]) + int(dfSeasonPlacement.loc[2,racer])
    dfAllTimePlacement.loc[3,racer] = int(dfAllTimePlacement.loc[3,racer]) + int(dfSeasonPlacement.loc[3,racer])







  #all data is now combined, so do any calculations for stats :)
  
  #Players Seasonal stats
    seasonalTotalPoints = 0
    seasonalTotalRaces = 0
    seasonalTracksOwned = 0
    for track in TrackIndex:
      seasonalTotalPoints = seasonalTotalPoints + int(dfSeasonScores.loc[TrackIndex[track],player])
      seasonalTotalRaces = seasonalTotalRaces + int(dfSeasonRaceCount.loc[TrackIndex[track],player])
      if (getTrackOwner(dfSeasonScores,dfSeasonRaceCount,track,TrackIndex) == player):
        seasonalTracksOwned = seasonalTracksOwned + 1

      #fixes divide by 0 error
      if seasonalTotalRaces == 0:
        seasonalAverage = 0
        seasonalFirstPlaceRate = 0
        seasonalAvgGPScore= 0
      else:
        seasonalAverage = seasonalTotalPoints/seasonalTotalRaces
        seasonalFirstPlaceRate = (int(dfSeasonWins.at[0,player]) / (seasonalTotalRaces/8))*100
        seasonalAvgGPScore = (seasonalTotalPoints) / (seasonalTotalRaces/8)

    #-----Players AllTime stats-----------
    allTimeTotalPoints = 0
    allTimeTotalRaces = 0
    allTimeTracksOwned = 0
    for track in TrackIndex:
      allTimeTotalPoints =  allTimeTotalPoints + int(dfAllTimeScores.loc[TrackIndex[track],player])
      allTimeTotalRaces =  allTimeTotalRaces + int(dfAllTimeRaceCount.loc[TrackIndex[track],player])
      if (getAllTimeTrackOwner(dfAllTimeScores,dfAllTimeRaceCount,track,TrackIndex) == player):
         allTimeTracksOwned =  allTimeTracksOwned + 1

      #fixes divide by 0 error
      if  allTimeTotalRaces == 0:
        allTimeAverage = 0
        allTimeFirstPlaceRate = 0
        allTimeAvgGPScore= 0
      else:
        allTimeAverage =  allTimeTotalPoints/ allTimeTotalRaces
        allTimeFirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (allTimeTotalRaces/8))*100
        allTimeAvgGPScore = (allTimeTotalPoints) / ( allTimeTotalRaces/8)
  
  print("Even More Calculations....")
  

  #placement stats
  seasonaltop1 = int(dfSeasonPlacement.at[0,player])
  seasonaltop2 = int(dfSeasonPlacement.at[1,player])
  seasonaltop3= int(dfSeasonPlacement.at[2,player])
  seasonaltop4 = int(dfSeasonPlacement.at[3,player])
  allTimetop1 = int(dfAllTimePlacement.at[0,player])
  allTimetop2 = int(dfAllTimePlacement.at[1,player]) 
  allTimetop3 = int(dfAllTimePlacement.at[2,player])
  allTimetop4 = int(dfAllTimePlacement.at[3,player])


  #gets all of the all time leaderboards (10), this is needed all the way up here so that the players seed can be found
  dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1 = getAllTimeLeaderboads(dfSeasonOwnedScore,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,
                                                                                                                                                                                                            dfAllTimeOwnedScore,dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeSeeding,TrackIndex,display = False)

  #generation of the seasonal and all time placement leaderboards for count 
  dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth = getPlacementLeaderboards(dfSeasonPlacement,display = False)
  dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth = getPlacementLeaderboards(dfAllTimePlacement,display = False)

  ##do percentages here


  #all of the stats are generated, so create the files
  #---------GENERATING THE HTML FILE---------

  #for output redirection later
  print('Generating HTML File...')
  default_stdout = sys.stdout

  #HTML File name and redirecting output
  filename = player + '.html'
  sys.stdout = open(filename, 'w')


  #---initalize HTML file with stlyles and headers
  htmlHeaders()
  
  #----HTML Page Order for the PDF (these can be changed if the order wants to be changed)---
  
  ##Creates the first page of the PDF, has the player name, and thier seasonal and all time stats. #find what is needed and pass them in
  coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonaltop1,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimetop1,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1,
  seasonaltop2,seasonaltop3,seasonaltop4,allTimetop2,allTimetop3,allTimetop4) 
  

  #KVR History Page
  KVRHistoryPage(player,dfKVR)

  GPStatsPage(player,dfSeasonWins,dfAllTimeWins)

  #shows all of the current and all time track mvps
  trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount) 

  trackStatsPage(dfSeasonScores,dfSeasonRaceCount,dfAllTimeScores,dfAllTimeRaceCount,TrackIndex)

  #pages with seasonal leaderbaords
  seasonalLeaderboardPage(TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth,dfSeasonOwnedScore) 

  #pages with all time boards
  allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1,dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth)  

    
  awardsPage(player) #a page with the player awards

  #print the info page at the end
  InfoPage()

 #----------Setting Output back to console--------
  sys.stdout = default_stdout
  print('Generation Complete')
  return filename


#CODE FOR MAKING PAGES GOES BELOW

def htmlHeaders():
  #file headers
  print('<!DOCTYPE html>')
  print('<html>')
  print('<body>')
  #divs for text

  print('<style> div.center {text-align: center; } </style>')
  print('<style> div.bar { display: flex; align-items: center; width: 100%; height: 3px; background-color: #1faadb; padding: 4px;} </style>')
  print('<style> div.left {text-align: left; } </style>')
  print('<style> div.statbox {text-align: left; display: inline-block; align-items:left; width: 30%; height: 320px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')
  print('<style> div.leaderboard {text-align:center; display: inline-block; align-items:center; width: 45%; height: 1150px; border: 1px solid black; padding: 4px; margin: auto; vertical-align: top; margin:auto;} </style>')
  print('<style> div.empty {display: flex; width: 100%; height: 15px;} </style>')
  print('<style> div.statbox2 {text-align: left; display: inline-block; align-items:left; width: 30%; height: 325px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;text-overflow: ellipsis;white-space: nowrap;overflow: hidden; } </style>')
  print('<style> .arrow {border: solid black;border-width: 0 3px 3px 0;display: inline-block;padding: 3px;} .up {transform: rotate(-135deg); -webkit-transform: rotate(-135deg); border: solid green;border-width: 0 3px 3px 0;}.down {transform: rotate(45deg);-webkit-transform: rotate(45deg); border: solid red; border-width: 0 3px 3px 0;} </style>')
  print('<style> div.statbox3 {text-align: left; display: inline-block; align-items:left; width: 30%; height: 375px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')
  print('<style> div.horizontalgap {float: left; overflow: hidden; height: 1px; width: 0px;} </style>')
  print('<style> div.vbar { display: flex; align-items: center; width: 3px; height: 200px; background-color: #1faadb; padding: 4px;} </style>')

  print('<style> div.statbox4 {text-align: left; display: inline-block; align-items:left; width: 13%; height: 500px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')


def coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonaltop1,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimetop1,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1,
  seasonaltop2,seasonaltop3,seasonaltop4,allTimetop2,allTimetop3,allTimetop4):
 
  #header
  print("<div class=\"center\">")
  print('<h1> Kartnite Profile:', player, '</h1>')
  print('<h3> Player Stats as of: ', date.today(), '</h3>')
  print('<p> PDF generated by Pat Marinich </p>')
  print('</div>')

  #break line
  print('<div class = \"bar\"> </div>')


  #gets the seed of the player
  playerIndex = dfPowerPoints1.index[dfPowerPoints1['Player']==player].tolist()
  seedingList = dfPowerPoints1['Seeding Power Points'].rank(ascending = False)
  playerSeed = seedingList[playerIndex]
  
  print("<div class=\"center\">")
  print('<h3> You are the all-time', int(playerSeed.iloc[0]),'seed! </h3>')
  print('</div>')
  #vertical bar
  print("<div class=\"bar\">")
  print('</div>')

  #seasonal stats
  print("<div class=\"center\">")
  print('<h1> Seasonal Stats </h1>')
  print('</div>')

  #centers the boxes

  print('<div class = \"center\">')
  #stat box left for race stats
  print("<div class=\"statbox\">")
  #title for race stats
  print("<div class=\"center\">")
  print('<h2> Race Stats </h2>')
  print('</div>')
  #STATS HERE
  greenCount = 0
  print('<p>Total Race Points: ', seasonalTotalPoints,'</p>',) 
  print('<p>Total Race Count: ', seasonalTotalRaces,'</p>')
  #if statement for triangles
  if( seasonalAverage >= allTimeAverage):
    print('<p>Average Placement Points: ', seasonalAverage, '<i class="arrow up"></i>','</p>')
    greenCount = greenCount + 1
  else:
     print('<p>Average Placement Points: ', seasonalAverage, '<i class="arrow down"></i>','</p>')

  print('<p>First Places: ', seasonaltop1,'</p>')
  print('<p>Top 2 Finishes: ', seasonaltop2,'</p>')
  print('<p>Top 3 Finishes: ', seasonaltop3,'</p>')
  print('<p>Top 4 Finishes: ', seasonaltop4,'</p>')
  print('</div>')

  #stat box center for GP
  print("<div class=\"statbox\">")
  #title for GP stats
  print("<div class=\"center\">")
  print('<h2> GP Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p> Total GP Wins:', dfSeasonWins.at[0,player],'</p>')
  print('<p> Total GPs Played:', seasonalTotalRaces/8,'</p>')
  
  #if statements for triangles
  if(seasonalFirstPlaceRate >= allTimeFirstPlaceRate):
    print('<p> GP First Place Rate: ', seasonalFirstPlaceRate , '% <i class="arrow up"></i> </p>'  )
    greenCount = greenCount + 1
  else:
     print('<p> GP First Place Rate: ', seasonalFirstPlaceRate , '% <i class="arrow down"></i> </p>'  )
  if(seasonalAvgGPScore >= allTimeAvgGPScore):
    print('<p> Average GP Score: ', seasonalAvgGPScore,'<i class="arrow up"></i>','</p>')
    greenCount = greenCount + 1
  else:
    print('<p> Average GP Score: ', seasonalAvgGPScore,'<i class="arrow down"></i>','</p>')
  
  print('</div>')

  #stat box right for MISC stats
  print("<div class=\"statbox\">")
  #title for MISC
  print("<div class=\"center\">")
  print('<h2> Misc Stats </h2>')
  print('</div>')
  #stats here
  #if statement for triangle
  if(seasonalTracksOwned >= allTimeTracksOwned):
    print('<p>#1 Player on a Track: ', seasonalTracksOwned,'<i class="arrow up"></i>''</p>')
    greenCount = greenCount + 1
  else:
    print('<p>#1 Player on a Track: ', seasonalTracksOwned,'<i class="arrow down"></i>''</p>')
  print('<p>Shock Dodges:', dfSeasonShock.at[0,player])
  print('<p>Times Hit By A Blue Shell:', dfSeasonBlue.at[0,player],'</p>')
  print('<p>Blue Dodges: ', dfSeasonBlue.at[1,player],'</p>')
  print('<p>Races Played on Owned Track:', float(dfSeasonOwnedScore.at[0,player])/4,'</p>')
  print('</div>')

  #end center
  print('</div>')

  #empty space bar
  print("<div class=\"empty\">")
  print('</div>')

  #message based on current preformance
  ##center these messages
  print("<div class=\"center\">")
  if(greenCount == 4):
    print('<p>You are on fire this season! Keep it up!</p>')
  elif(greenCount == 3):
    print('<p> This season is looking good for you so far!</p>')
  elif(greenCount == 2):
    print('<p>You are playing to your standard, good job!</p>')
  elif(greenCount == 1):
    print('<p>It looks like you are on a cold streak, you\'ll get them next time!</p>')
  else:
    print('<p>Yikes, looks like you have to be good to be lucky </p>')
  print('</div>')
  
  #vertical bar
  print("<div class=\"bar\">")
  print('</div>')

  #----All time stats----
  #seasonal stats
  print("<div class=\"center\">")
  print('<h1> All-Time Stats </h1>')
  print('</div>')

  #centers the boxes
  print('<div class = \"center\">')
  #stat box left for race stats
  print("<div class=\"statbox\">")
  #title for race stats
  print("<div class=\"center\">")
  print('<h2> All-Time Race Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p>Total Race Points: ',  allTimeTotalPoints, '</p>')

  #getting the races for player post season 3
  sub = 0
  if player in PLAYER_RACES_DICT.keys():
    sub = PLAYER_RACES_DICT[player]
  
  print('<p>Total Race Count: ',  allTimeTotalRaces, ' (' + str(allTimeTotalRaces-sub) + ')','</p>')
  print('<p>Average Placement Points: ',  allTimeAverage,'</p>')
  print('<p>First Places: ',  allTimetop1,'</p>')
  print('<p>Top 2 Finishes: ',  allTimetop2,'</p>')
  print('<p>Top 3 Finishes: ',  allTimetop3,'</p>')
  print('<p>Top 4 Finishes: ',  allTimetop4,'</p>')

  print('</div>')

  #stat box center for GP
  print("<div class=\"statbox\">")
  #title for GP stats
  print("<div class=\"center\">")
  print('<h2> All-Time GP Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p> Total GP Wins:', dfAllTimeWins.at[0,player],'</p>')
  print('<p> Total GPs Played:', allTimeTotalRaces/8,'</p>')
  print('<p> GP First Place Rate: ',  allTimeFirstPlaceRate , '% </p>'  )
  print('<p> Average GP Score: ',  allTimeAvgGPScore,'</p>')
  print('</div>')

  #stat box right for MISC stats
  print("<div class=\"statbox\">")
  #title for MISC
  print("<div class=\"center\">")
  print('<h2> All-Time Misc Stats </h2>')
  print('</div>')
  #stats here
  print('<p>#1 Player on a Track: ',  allTimeTracksOwned,'</p>')
  print('<p>Shock Dodges:', dfAllTimeShock.at[0,player])
  print('<p>Times Hit By A Blue Shell:', dfAllTimeBlue.at[0,player],'</p>')
  print('<p>Blue Dodges: ', dfAllTimeBlue.at[1,player],'</p>')
  print('<p>Races Played on Owned Track:', float(dfAllTimeOwnedScore.at[0,player])/4,'</p>')
  print('</div>')

  #end center
  print('</div>')


  print('<br>')
  print('<div class=\"bar\"> </div>')

  #add the badges under the last bar 

  #getting the seasonal and all time badges
  swPath = ""
  awPath = ""
  sgpPath = ""
  agpPath = ""
  sbPath = ""
  abPath = ""
  #seasonal wins
  if seasonaltop1 > 4999:
    swPath = "Badges\\RaceWins\\Win5kRaces.png"
  elif seasonaltop1 > 2499:
    swPath = "Badges\\RaceWins\\Win2.5kRaces.png"
  elif seasonaltop1 > 999:
    swPath = "Badges\\RaceWins\\Win1kRaces.png"
  elif seasonaltop1 > 499:
    swPath = "Badges\\RaceWins\\Win500Races.png"
  elif seasonaltop1 > 249:
    swPath = "Badges\\RaceWins\\Win250Races.png"
  elif seasonaltop1 > 99:
    swPath = "Badges\\RaceWins\\Win100Races.png"
  elif seasonaltop1 > 49:
    swPath = "Badges\\RaceWins\\Win50Races.png"
  elif seasonaltop1 > 9:
    swPath = "Badges\\RaceWins\\Win10Races.png"
  elif seasonaltop1 > 0:
    swPath = "Badges\\RaceWins\\Win1Race1.png"
  #all time wins
  if allTimetop1 > 4999:
    awPath = "Badges\\RaceWins\\Win5kRaces.png"
  elif allTimetop1 > 2499:
    awPath = "Badges\\RaceWins\\Win2.5kRaces.png"
  elif allTimetop1 > 999:
    awPath = "Badges\\RaceWins\\Win1kRaces.png"
  elif allTimetop1 > 499:
    awPath = "Badges\\RaceWins\\Win500Races.png"
  elif allTimetop1 > 249:
    awPath = "Badges\\RaceWins\\Win250Races.png"
  elif allTimetop1 > 99:
    awPath = "Badges\\RaceWins\\Win100Races.png"
  elif allTimetop1 > 49:
    awPath = "Badges\\RaceWins\\Win50Races.png"
  elif allTimetop1 > 9:
    awPath = "Badges\\RaceWins\\Win10Races.png"
  elif allTimetop1 > 0:
    awPath = "Badges\\RaceWins\\Win1Race1.png"

  #Gp Wins seasonal
  if int(dfSeasonWins.at[0,player]) > 999:
    sgpPath = "Badges\\GPWins\\Win1000GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 499:
    sgpPath = "Badges\\GPWins\\Win500GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 249:
    sgpPath = "Badges\\GPWins\\Win250GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 99:
    sgpPath = "Badges\\GPWins\\Win100GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 49:
    sgpPath = "Badges\\GPWins\\Win50GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 24:
    sgpPath = "Badges\\GPWins\\Win25GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 9:
    sgpPath = "Badges\\GPWins\\Win10GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 4:
    sgpPath = "Badges\\GPWins\\Win5GPs.png"
  elif int(dfSeasonWins.at[0,player]) > 0:
    sgpPath = "Badges\\GPWins\\Win1GP.png"
    
  #all time gps
  if int(dfAllTimeWins.at[0,player]) > 999:
    agpPath = "Badges\\GPWins\\Win1000GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 499:
    agpPath = "Badges\\GPWins\\Win500GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 249:
    agpPath = "Badges\\GPWins\\Win250GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 99:
    agpPath = "Badges\\GPWins\\Win100GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 49:
    agpPath = "Badges\\GPWins\\Win50GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 24:
    agpPath = "Badges\\GPWins\\Win25GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 9:
    agpPath = "Badges\\GPWins\\Win10GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 4:
    agpPath = "Badges\\GPWins\\Win5GPs.png"
  elif int(dfAllTimeWins.at[0,player]) > 0:
    agpPath = "Badges\\GPWins\\Win1GP.png"
    
  #seasonal blue
  if int(dfSeasonBlue.at[0,player]) > 4999:
    sbPath = "Badges\\BlueShells\\5kBlues.png"
  elif int(dfSeasonBlue.at[0,player]) > 2499:
    sbPath = "Badges\\BlueShells\\2.5kBlues.png"
  elif int(dfSeasonBlue.at[0,player]) > 999:
    sbPath = "Badges\\BlueShells\\1kBlues.png"
  elif int(dfSeasonBlue.at[0,player]) > 499:
    sbPath = "Badges\\BlueShells\\500Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 249:
    sbPath = "Badges\\BlueShells\\250Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 99:
    sbPath = "Badges\\BlueShells\\100Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 49:
    sbPath = "Badges\\BlueShells\\50Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 24:
    sbPath = "Badges\\BlueShells\\25Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 9:
    sbPath = "Badges\\BlueShells\\10Blues.png"
  elif int(dfSeasonBlue.at[0,player]) > 0:
    sbPath = "Badges\\BlueShells\\1Blue.png"

  #all time blue
  if int(dfAllTimeBlue.at[0,player]) > 4999:
    abPath = "Badges\\BlueShells\\5kBlues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 2499:
    abPath = "Badges\\BlueShells\\2.5kBlues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 999:
    abPath = "Badges\\BlueShells\\1kBlues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 499:
    abPath = "Badges\\BlueShells\\500Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 249:
    abPath = "Badges\\BlueShells\\250Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 99:
    abPath = "Badges\\BlueShells\\100Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 49:
    abPath = "Badges\\BlueShells\\50Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 24:
    abPath = "Badges\\BlueShells\\25Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 9:
    abPath = "Badges\\BlueShells\\10Blues.png"
  elif int(dfAllTimeBlue.at[0,player]) > 0:
    abPath = "Badges\\BlueShells\\1Blue.png"



  if swPath == "":
    swPath = 'Badges\\noBadge.jpg'
  if awPath == "":
    awPath = 'Badges\\noBadge.jpg'
  if sgpPath == "":
    sgpPath = 'Badges\\noBadge.jpg'
  if agpPath == "":
    agpPath = 'Badges\\noBadge.jpg'
  if sbPath == "":
    sbPath = 'Badges\\noBadge.jpg'
  if abPath == "":
    abPath = 'Badges\\noBadge.jpg'


  #display the badges if applicable
  print("<div class=\"center\">")
  print('<h2> Seasonal Badges <span style="display:inline-block; width: 300px;"></span> All-Time Badges </h2>')
  print('</div>')
  print('<br>')

  print("<div class=\"center\">")
  print('<img src=', PATH_EXT+swPath, 'alt=\"Seasonal Wins\" width=\"130\" height=\"130\">' )
  print('<img src=', PATH_EXT+sgpPath, 'alt=\"Seaonsal GP Wins\" width=\"130\" height=\"130\">' )
  print('<img src=', PATH_EXT+sbPath, 'alt=\"Seasonal Blues\" width=\"130\" height=\"130\">')

  #horizontal bar
  print('<span style="display:inline-block; width: 85px;"></span>')
  #print("<div class=\"vbar\">")
  #print("</div>")

  print('<img src=', PATH_EXT+awPath, 'alt=\"Seasonal Wins\" width=\"130\" height=\"130\">' )
  print('<img src=', PATH_EXT+agpPath, 'alt=\"Seaonsal GP Wins\" width=\"130\" height=\"130\">' )
  print('<img src=', PATH_EXT+abPath, 'alt=\"Seasonal Blues\" width=\"130\" height=\"130\">' )

  print("</div>")


  
    
    
    
    
    
    
    
    
    
    
    










 

def trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount):
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  print('<div class =\"center\">')
  #header
  print('<h1> Track MVPs </h1>')

  #seasonal

  print("<div class=\"leaderboard\">")
  print('<div class =\"center\">')
  print('<h2> Seasonal MVPs </h2>')
  #gets all the seasonal mvps, the the to_html prints the html nessassary
  dfSeasonOwners = getAllTrackOwners(dfSeasonScores,dfSeasonRaceCount,TrackIndex, display= False)
  print(dfSeasonOwners.to_html())
  print('</div>')
  print('</div>')

  #all time MVPs
  print("<div class=\"leaderboard\">")
  print('<div class =\"center\">')
  print('<h2> All-Time MVPs </h2>')
  #same as above conversion to html from pandas
  dfAllTimeOwners = getAllTimeAllTrackOwners(dfAllTimeScores,dfAllTimeRaceCount,TrackIndex, display= False)
  print(dfAllTimeOwners.to_html())
  print('</div>')
  print('</div>')


  #end center
  print('</div>')

  #ending bar
  print('<br>')
  print('<div class=\"bar\"> </div>')

def seasonalLeaderboardPage(TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth,dfSeasonOwnedScore):

  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  
  #header
  print('<div class =\"center\">')
  print('<h1> Seasonal Leaderboards </h1>')
  print('</div>')

  #stat boxes for seasonal leaderboards

  #generate the leaderboards
  kartSeasonalLeaderboard= getSeedings(dfSeasonOwnedScore,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,TrackIndex,display = False)
  PPRLeaderboard = getPointsPerRace(dfSeasonScores,dfSeasonRaceCount,TrackIndex,display = False)
  raceCountLeaderboard = getRaceCountLeaderbaords(dfSeasonRaceCount, TrackIndex,display = False)
  GPWinsLeaderboard = getGPWinsLeaderboard(dfSeasonWins,display = False)
  shockLeaderboard = getShockDodges(dfSeasonShock,display = False)
  blueLeaderboard = getBlueLeaderboard(dfSeasonBlue,display = False)

  #box 1 kart score
  print('<div class = \"center\">')
  print("<div class=\"statbox2\">")
  print('<h2> Kart Score </h2>')
  print(kartSeasonalLeaderboard.to_html())
  print('</div>')
  #box 2 player average
  print("<div class=\"statbox2\">")
  print('<h2> Player Average</h2>')
  print(PPRLeaderboard.to_html())
  print('</div>')
  #box 3 Race Count
  print("<div class=\"statbox2\">")
  print('<h2> Race Count </h2>')
  print(raceCountLeaderboard.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #box 4 GP Wins
  print("<div class=\"statbox2\">")
  print('<h2> GP Wins</h2>')
  print(GPWinsLeaderboard.to_html())
  print('</div>') 
  #box 5
  print("<div class=\"statbox2\">")
  print('<h2> Shock Dodges </h2>')
  print(shockLeaderboard.to_html())
  print('</div>')
  #box 6
  print("<div class=\"statbox2\">")
  print('<h2> Blue Shells </h2>')
  print(blueLeaderboard.to_html())
  print('</div>')
  print('</div>')

  #bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')
  
  #first places
  print("<div class=\"statbox2\">")
  print('<h2> First Place Finishes </h2>')
  print(dfSeasonFirst.to_html())
  print('</div>') 
  #second places
  print("<div class=\"statbox2\">")
  print('<h2> Top 2 Finishes </h2>')
  print(dfSeasonSecond.to_html())
  print('</div>')
  #third places
  print("<div class=\"statbox2\">")
  print('<h2> Top 3 Finishes </h2>')
  print(dfSeasonThird.to_html())
  print('</div>')
  print('</div>')

  #bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')

  #Fourth places
  print("<div class=\"statbox2\">")
  print('<h2> Top 4 Finishes </h2>')
  print(dfSeasonFourth.to_html())
  print('</div>')
  print('</div>')


  ##percentages go here

  #end of pahe bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')

def allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1,dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth):

  #Page 4, All-Time Leaderboards
 
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #header
  print('<div class =\"center\">')
  print('<h1> All-Time Leaderboards </h1>')
  print('</div>')

  
  print('<div class = \"center\">')
  #statbox 1 power points
  print("<div class=\"statbox2\">")
  print('<h2> Seed Power Points</h2>')
  print(dfPowerPoints1.to_html())
  print('</div>')
  #statbox 2 kart Score
  print("<div class=\"statbox2\">")
  print('<h2> Kart Score </h2>')
  print(dfNormalizedKart1.to_html())
  print('</div>')
  #statbox 3 kart rating
  print("<div class=\"statbox2\">")
  print('<h2> Kart Rating</h2>')
  print(dfKartRating1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 4 misc scores
  print("<div class=\"statbox2\">")
  print('<h2> Misc Points</h2>')
  print(dfMiscScore1.to_html())
  print('</div>')
  #statbox 5 all time wins
  print("<div class=\"statbox2\">")
  print('<h2> GP Wins</h2>')
  print(dfAllTimeWins1.to_html())
  print('</div>')
  #statbox 6 average
  print("<div class=\"statbox2\">")
  print('<h2> Average Points</h2>')
  print(dfAllTimeAverage1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 7 shock dodges
  print("<div class=\"statbox2\">")
  print('<h2> Shock Dodges</h2>')
  print(dfAllTimeShockDodges1.to_html())
  print('</div>')
  #statbox 8  blue shells
  print("<div class=\"statbox2\">")
  print('<h2> Blue Shells</h2>')
  print(dfAllTimeBlueShells1.to_html())
  print('</div>')
  #statbox 9 race count
  print("<div class=\"statbox2\">")
  print('<h2> Race Count</h2>')
  print(dfAllTimeRaceCount1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #disclamer on the stat being tracked
  print('<div class =\"center\">')
  print("<h7> Placement Stats Started Season 3 </h7>")
  print('<br>')
  print('</div>')

  #statbox first places
  print("<div class=\"statbox2\">")
  print('<h2> First Place Finishes</h2>')
  print(dfAllTimeFirst.to_html())
  print('</div>')
  #statbox second places
  print("<div class=\"statbox2\">")
  print('<h2> Top 2 Finsihes</h2>')
  print(dfAllTimeSecond.to_html())
  print('</div>')
  #statbox 3rd places
  print("<div class=\"statbox2\">")
  print('<h2> Top 3 Finishes </h2>')
  print(dfAllTimeThird.to_html())
  print('</div>')


  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 4th places
  print("<div class=\"statbox2\">")
  print('<h2> Top 4 Finishes </h2>')
  print(dfAllTimeFourth.to_html())
  print('</div>')


  #statbox points scored
  print("<div class=\"statbox2\">")
  print('<h2> Total Points</h2>')
  print(dfAllTimeTotalPoints1.to_html())
  print('</div>')
  print('</div>')


  #break line for page
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

def awardsPage(player):

  #page split Awards time
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')


  
  #header
  print('<div class =\"center\">')
  print('<h1> Award Trophy Case </h1>')
  print('</div>')
  #bar
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #all of the players awards
  print('<ul>')
  for season in AWARD_LIST[player]:
    for award in season:
      print('<li>', award, '</li>')
  print('</ul>')

  #bar
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')


def KVRHistoryPage(player,dfKVR):
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #page header
  #header
  print('<div class =\"center\">')
  print('<h1> Kart Versus Rating History (KVR) </h1>')
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')

  #center the graph
  print('<div class =\"center\">')
  #get the embedded HTML for the plot
  make_line_plot(dfKVR,player)
  

  path = 'KVRHistory.png'
  
  print('<img src=', PATH_EXT+path, 'alt=\"KVR History\" width=\"1000\" height=\"800\">' )
  print('</div>')

  #make table of all players KVR HERE
  print('<div class =\"center\">')
  kvrCurrentLeaderboard, KVRAllTimeLeaderboard = getKVRLeaderBoards(dfKVR)
  print("<div class=\"statbox3\">")
  print('<h2> Current KVR </h2>')
  print(kvrCurrentLeaderboard.to_html())
  print('</div>')

  print("<div class=\"statbox3\">")
  print('<h2> All Time High KVR </h2>')
  print(KVRAllTimeLeaderboard.to_html())
  print('</div>')

  #----DO THE CALCULATION FOR RACE SIM--------
  #make the 3 groups of 3
  top3 = []
  second3=[]
  third3=[]
  for idx in kvrCurrentLeaderboard.index:
    if kvrCurrentLeaderboard['Player'][idx] != player:
      if len(top3) != 3:
        top3.append((kvrCurrentLeaderboard['Player'][idx],kvrCurrentLeaderboard['Current KVR'][idx]))
      elif len(second3) != 3:
        second3.append((kvrCurrentLeaderboard['Player'][idx],kvrCurrentLeaderboard['Current KVR'][idx]))
      elif len(third3) != 3:
        third3.append((kvrCurrentLeaderboard['Player'][idx],kvrCurrentLeaderboard['Current KVR'][idx]))
      else:
        break
  c_kvr  = (kvrCurrentLeaderboard.loc[kvrCurrentLeaderboard['Player'] == player])['Current KVR'].item()
  #so now we have player and KVRs
  top3.insert(0,(player,c_kvr))
  second3.insert(0,(player,c_kvr))
  third3.insert(0,(player,c_kvr))

  race1 = []
  race2 = []
  race3 = []
    
  for p in top3:
    race1.append(int(p[1]))
  while len(race1) != 12:
    race1.append(5000)

  for p in second3:
    race2.append(int(p[1]))
  while len(race2) != 12:
    race2.append(5000)

  for p in third3:
    race3.append(int(p[1]))
  while len(race3) != 12:
    race3.append(5000)
    
  win1 = getEVArr(race1)
  win2 = getEVArr(race2)
  win3 = getEVArr(race3)
  place1 = getPlacementExpected(win1)
  place2 = getPlacementExpected(win2)
  place3 = getPlacementExpected(win3)

  place1 = list(map(lambda x: round(x,2),place1))
  place2 = list(map(lambda x: round(x,2),place2))
  place3 = list(map(lambda x: round(x,2),place3))


  #-----------------------------------

  #statbox for the new calculation
  print("<div class=\"statbox3\">")
  print('<div class =\"center\">')
  print('<h2> Race Simulations </h2>')
  print("<h4> Based on KVR Only </h4>")
  print('</div>')
  
  print("<p> <b> Race 1: </b> You,",str(top3[1][0])+',',str(top3[2][0])+', and',str(top3[3][0]),'</p>')
  print("<p> You are expected<b>", str(place1[0]), "</b>place or<b>", round(pointsExpected(place1[0]),2), "</b>points </p>" )
  print("<p> <b> Race 2: </b> You,",str(second3[1][0])+',',str(second3[2][0])+', and',str(second3[3][0]),'</p>')
  print("<p> You are expected<b>", str(place2[0]), "</b>place or<b>", round(pointsExpected(place2[0]),2), "</b>points </p>" )
  print("<p> <b> Race 3: </b> You,",str(third3[1][0])+',',str(third3[2][0])+', and',str(third3[3][0]),'</p>')
  print("<p> You are expected<b>", str(place3[0]), "</b>place or<b>", round(pointsExpected(place3[0]),2), "</b>points </p>" )

  
  print('</div>')


  print('</div>')




def GPStatsPage(player,dfSeasonGP,dfAllTimeGP):
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  print('<div class =\"center\">')
  print('<h1> Kartnite Grand Prix Stats </h1>')
  print('</div>')

  #break line
  print('<br>')
  print('<div class = \"bar\"> </div>')

  #center the graph
  print('<div class =\"center\">')
  #get the embedded HTML for the plot
  make_GP_pie_charts(dfSeasonGP,dfAllTimeGP,player)
  
  path = 'GPWins.png'
  

  print('<img src=', PATH_EXT+path, 'alt=\"GP STATS\" width=\"1000\" height=\"1250\">' )
  print('</div>')

  print('<div class = \"bar\"> </div>')


def InfoPage():
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #Header
  print('<div class =\"center\">')
  print('<h1> Infromation Page </h1>')
  print('</div>')

  #The different stats 
  #KVR
  print('<b> Kartnite Versus Raiting (KVR) </b>')
  print('<ul>')
  print('<li>Inspired by the Chess ELO rating scale and the MKWii VR system.</li>')
  print('<li>The KVR number represents a probablity that a player will beat another given player in a race.</li>')
  print('<li>The probablity player A beats player B is defined by: 0.5 + (0.5 * (1-e<sup>(-1/2500)*(Player A KVR - Player B KVR)</sup>)) </li>')
  print('<li>This is approximatly a 10 percent change every 500 points. </li>')
  print('<li>As a reference point the COMs are at 5000 KVR with a small variace every given race (+- 250 points) </li>')
  print('<li>To calculate the KVR change after a race, a players expected placement is calculated using the their KVR compared to each other player</li>')
  print('<li>Then if a player gets a placement higher then expected, KVR will go up by the difference (times a scale factor of 20) and vice versa if they do worse then the expected placement. </li>')
  print('</ul>')

  #TRACK MVPs
  print('<b> Track MVP </b>')
  print('<ul>')
  print('<li>Track MVP determines who is the best player on each track either seasonally or all-time</li>')
  print('<li>For Seasonal: It is determined by (0.96)*(Player Track Average) + 0.04(Total Track Points)</li>')
  print('<li>For All-Time: It is strictly determined by Player Track Average, however there is a minimum race count of 5</li>')
  print('<li>The reason is it calculated slightly differently is to ensure fairness in both the short term and long term</li>')
  print('<li>For Seasonal: It would be unfair if one player went 1/1 and another went 14/15, as due to sample size, the 14/15 result is much better, thus having a small percentage of total score count solves this problem</li>')
  print('<li>For Seasonal: A race minimum would not work as well here due to the asymmetry of race count among players and tracks in a short time frame</li>')
  print('<li>For All-Time: Having a race minimum accomplishes this due to it being long term with a large sample size</li>')
  print('</ul>')
  #Kart Score
  print('<b> Kart Score </b>')
  print('<ul>')
  print('<li>Kart Score is a seasonal stat which takes into account six different catigories</li>')
  print('<li>The catigories are: GP Wins, Track MVP Points, Race Points, Track Average Points, Shock Dodge Points, and Blue Shell Points</li>')
  print('<li>These are the points given out as it currently stands: </li>')
  print('<ul>')
  print('<li>Each GP Point Scored: 1</li>')
  print('<li>Each GP Win: 100</li>')
  print('<li>Each Time A Track you are MVP of is Played: 0.5 Points Per Player </li>')
  print('<li>Each Shock Dodge: 5</li>')
  print('<li>Each Blue Shell: 0.5</li>')
  print('<li>Each Blue Dodge: 10</li>')
  print('<li>Average Score: 1 Point Per Average</li>')
  print('</ul>')
  print('<li>There is also Normalized Kart Score for the All Time Stats</li>')
  print('<li>This is calculated by having your seasonal kart score converted into a percentage of the total kart score earned this current season</li>')
  print('<li>Then this is added to the previous seasonal scores decermented by 15 percent for each season that is has passed.</li>')
  print('<li>For example if it was season 4 the normalized kart score would be: This Seasons Score + 0.85(Last Season) + .7225(2 Seasons Ago) + 0.61(3 Seasons Ago)</li>')
  print('</ul>')

  #Kart Rating
  print('<b> Kart Rating </b>')
  print('<ul>')
  print('<li>A stat inspired by QBR from football</li>')
  print('<li>A maximum Kart Raiting is 160 points </li>')
  print('<li>Up to 60 points are given from GP Win Percentage</li>')
  print('<li>Up to 60 Points are given from average placement</li>')
  print('<li>Up to 40 Points are given from Track MVPs</li>')
  print('<li>It is calculated by: 60(GP Win percentage) + 60(avg/15) + Track MVPs</li>')
  print('</ul>')

  #MISC Points
  print('<b> Miscellaneous Points </b>')
  print('<ul>')
  print('<li>Misc points is a stat whose goal is to keep track of the little things that happen each race</li>')
  print('<li>It takes into account Blue Shells, Blue Dodges, and Shock Dodges</li>')
  print('<li>It is calculated by:</li>')
  print('<ul>')
  print('<li>Each Blue Shell: 1</li>')
  print('<li>Each Blue Shell Dodge: 10</li>')
  print('<li>Each Shock Dodge: 4</li>')
  print('<li>Then this sum is divided by the GPs played so it acts as an average per GP</li>')
  print('</ul>')
  print('</ul>')

  #Seeding Power Points
  print('<b> Seeding Power Points </b>')
  print('<ul>')
  print('<li>The goal of this stat is to combine Kart Score, Kart Rating, and Misc Points into a singular metric.</li>')
  print('<li>The idea being that each of these individual stats have their flaws, but by combining them, they cover the flaws of one another</li>')
  print('<li>Seeding Power Points is calccuated by looking at a players location on the leaderboard for each of these stats and summing them up </li>')
  print('<li>4 Points are given for each position on the Kart Rating Leaderboard</li>')
  print('<li>3 Points are given for each position on the Normalized Kart Score Leaderboard</li>')
  print('<li>1 Point is given for each position on the Misc Score Leaderboard</li>')
  print('<li>Currently there are 11 players in the stats</li>')
  print('<li>Therefore the maximum SPP would be 4*11 + 3*11 + 11 = 88</li>')
  print('</ul>')


#The idea of this page is to provide the stats for each of the tracks, including 
#The race count and the best 3 players all time and seasonal
def trackStatsPage(dfSeasonScores,dfSeasonRaces,dfAllScores,dfAllRaces,TrackIndex):

  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #Header
  print('<div class =\"center\">')
  print('<h1> Track Stats </h1>')
  print('</div>')

  print('<div class = \"bar\"> </div>')
  
  count = 0
  #for each track
  for track in TrackIndex.keys():
    
    seasonRaces,allRaces,sMVP,allMVP = getTrackStats(dfSeasonScores,dfSeasonRaces,dfAllScores,dfAllRaces,track,TrackIndex)
    #put all of these into a box neatly
    
    sMVP = sMVP.iloc[0:3]
    allMVP = allMVP.iloc[0:3]

    if count % 6 == 0:
      print("<div class=\"center\">")

    print("<div class=\"statbox4\">")
    print('<h4>',track,'</h4>')
    print('<p> Seasonal Races:', seasonRaces, '</p>')
    print('<p> All-Time Races:', allRaces, '</p>')
    print('<p> Seasonal Best</p>')
    print(sMVP.to_html(index = False))
    print('<p> All-Time Best </p>')
    print(allMVP.to_html(index=False))
    print('</div>')

    if count % 6 == 5:
      print("</div>")

    count = count + 1
      
  print('<div class = \"bar\"> </div>')


    




#CREATE NEW PAGES HERE



#this function converts the html file into a pdf so it can be viewed nicely
def convertHTMLtoPDF(filename):
  print('Converting to PDF...')
  path = 'wkhtmltopdf.exe'
  config = pdfkit.configuration(wkhtmltopdf=path)

  # Returns the date for file name
  today = date.today()
  today = date.isoformat(today)

  #open the file
  currFile = open(filename, 'r')
  
  #Convert
  output = 'Kartnite Stats - ' + today + '.pdf'
  pdfkit.from_file(currFile, output_path=output, configuration=config,options={"enable-local-file-access": "",'--keep-relative-links': ''},verbose=True)
  print('Conversion Complete...')

  return output


def decode(word,shift):
    txt = ""
    for letter in word:
        if letter == '.' or letter == '@':
            txt += letter
            continue
        stayInAlphabet = ord(letter)-shift
        if stayInAlphabet < ord('a'):
            stayInAlphabet += 26   
        txt += (chr(stayInAlphabet))
    return txt


#this is for emailing the created PDF to the player that it was generated for
import yagmail
def sendReport(player,userEmail,userPass,message,pdfFile):

  print('Creating Email....')
  #A dictonary of Players Names and their prefered Email addresses
  # emails = {'Pat' : 'patrick.marinich@gmail.com',
  #           'Kevin' : 'kevinfrancisjr@gmail.com',
  #           'Chris' : 'chrispauldragone@gmail.com',
  #           'Demitri' : 'dforand20@gmail.com',
  #           'Joe' : 'frallerjo@gmail.com',
  #           'Karla' : 'karlavsetzer@gmail.com',
  #           'Callum' : 'Goaliecal50@gmail.com',
  #           'Shane' : 'shanemdunphy@hotmail.com'}
  emails = {'Pat' : 'grkiztb.drizezty@xdrzc.tfd',
'Kevin' : 'bvmzewiretzjai@xdrzc.tfd',
'Chris' : 'tyizjgrlcuirxfev@xdrzc.tfd',
'Demitri' : 'uwfireuCA@xdrzc.tfd',
'Joe' : 'wirccviaf@xdrzc.tfd',
'Karla' : 'bricrmjvkqvi@xdrzc.tfd',
'Callum' : 'XfrczvtrcFA@xdrzc.tfd',
'Shane' : 'jyrevdulegyp@yfkdrzc.tfd'}
  #the user inputs their email infromation, to send the email
  user = yagmail.SMTP(user=userEmail, password=userPass)

  # Returns the date for file name
  today = date.today()
  today = date.isoformat(today)

  #uses the dictionary to get the email for the reciepient
  user.send(to=decode(emails[player],17), subject=('Kartnite Stats from: ' +  today), contents=message,attachments = pdfFile)

  print('Report Delievered To ', player, '!')