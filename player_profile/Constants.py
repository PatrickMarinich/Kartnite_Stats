#this file will contain any constants that are used in other files, typically constants that are not directally used in a singular
#function will be used here as of now it is just a file to hold the player awards, but other things may be held here in the future

#---CREDITS and other info-------
VERSION = 'v4.2'
CONTRIBUTORS = 'Patrick Marinich'
#------------------------------------

#------------TRACK LIST-------------
#seeds are needed to preform the reset
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


#-----------KART SCORE---------
#Point Values, constants which can be adjusted for ease of balancing
POINTS_SCORED_POINTS = 1        #points for each GP point scored
GP_WINS_POINTS = 100               #points per gp win
OWNER_POINTS = 0.5              #points per player on owned track
DODGE_POINTS = 5                   #points per dodge
BLUE_POINTS = 1                 #points for getting hit with blue shell
BLUE_D_POINTS = 10                 #points for dodging a blue shell
#---------removed from this calculation-------
AVERAGE_POINTS = 0                #points for track average, (kart score should be a accumlative stat)
#--------------------------------------


#--------------KART RATING-----------
#kart rating is a new metric that acts like QBR in football,
#a max kart rating will be out of 160 points
#60 points will be from GP win %
#60 points will be from average GP points
#40 points will be from all time tracks owned
POINTS_FOR_WINS = 60
POINTS_FOR_AVERAGE = 60
POINTS_FOR_TRACK = 40
#---------------------------------------

#---------MISC POINTS----------
#For the miscellanous points stats, these are per interation,
#but the stat is calculated per 8 races
BLUE_DODGE = 10
BLUE_HIT = 1
SHOCK = 4
#----------------------


# Races Played Before Placementes were tracked, these will be used for accurate percentages and things
PAT_RACES = 748.0
CHRIS_RACES = 731.0
DEMITRI_RACES = 666.0
KEVIN_RACES = 508.0
JOE_RACES = 291.0     
MIKE_RACES = 53.0
SHANE_RACES = 24.0
JASON_RACES = 4.0
#for itneractive access use
PLAYER_RACES_DICT = {"Pat" : PAT_RACES, "Chris": CHRIS_RACES,"Demitri": DEMITRI_RACES, "Kevin": KEVIN_RACES, "Joe": JOE_RACES, "Mike": MIKE_RACES, "Shane": SHANE_RACES, "Jason":JASON_RACES}

#------------------------------
#SEASON GP WINS -> MANUALLY STORED BY 
#UPDATE THESE EVERY SEASON 
#UPDATE IF SOMEBODY NEW WINS A GP
PLAYER_GP_WINS_PAST_SEASONS = {"Pat" : [11,21,17,10,6,33,53],
                           "Chirs" : [4,8,5,16,5,11,17],
                           "Demitri" : [6,16,3,24,3,22,27],
                           "Kevin" : [10,27,17,37,14,46,60], 
                            "Shane": [0,0,0,0,1,0,0]}

#------------------------
#longest GP win streaks, manually tracking
PLAYER_GP_WIN_STREAKS = {
"Pat" : 14,
"Chris" : 3,
"Kevin" : 6,
"Demitri" : 3,
"Shane" : 1
}

#THESE ARE THE SEASONAL AWARDS

#---Season 1 (These were retroactive, voted on in season 4) -- 
PAT_RETRO_AWARDS = ['Season I \'2 Seed\'', 'Season I Best Shortcuts']
CHRIS_RETRO_AWARDS = ['Season I \'3 Seed\'']
KEVIN_RETRO_AWARDS = ['Season I \'1 Seed\'', 'Season I Best Items']
DEMITRI_RETRO_AWARDS = ['Season I Most Improved', 'Season I Rookie of the Year']
#---SEASON 2 (Awards started HERE)----
PAT_SEASON2_AWARDS = ['Season II Luckiest Player', 'Season II Best Sniper']
CHRIS_SEASON2_AWARDS = ['Season II Best Bagger', 'Season II Best Shortcuts', 'Season II Biggest Lacker', 'Season II Choke Artist', '*Season II Biggest Bum*']
KEVIN_SEASON2_AWARDS = ['Season II MVP', 'Season II Best Lines']
DEMITRI_SEASON2_AWARDS = ['Season II Best Trapper', 'Season II Best Reactions', 'Season II Best Guy', 'Season II Best Item User']
JOE_SEASON2_AWARDS = ['Season II Most Improved Player']
#---Season 3----
PAT_SEASON3_AWARDS = ['Season III Luckiest Player', 'Season III Best Shortcuts']
CHRIS_SEASON3_AWARDS =['Season III Best Sniper', 'Season III Best Lines', 'Season III Biggest Lacker', '*Season III Least Imporved Player*']
KEVIN_SEASON3_AWARDS =['Season III MVP','Season III Best Item User']
DEMITRI_SEASON3_AWARDS =['Season III Best Trapper','Season III Best Reactions', 'Season III Best Guy', 'Season III Choke Artist', '*Season III On Thin Ice*','*Season III Biggest Dissipointment*']
JOE_SEASON3_AWARDS = ['Season III Best Bagger', 'Season III Most Improved Player']
#----Season 4 awards----
PAT_SEASON4_AWARDS = ['Season IV Best Sniper', 'Season IV Best Shortcuts', 'Season IV Biggest Lacker']
CHRIS_SEASON4_AWARDS = ['Season IV Best Bagger', 'Season IV Best Lines', 'Season IV Choke Artist']
KEVIN_SEASON4_AWARDS = ['Season IV MVP', 'Season IV Best Item User', 'Season IV Best Trapper', 'Season IV Luckiest Player']
DEMITRI_SEASON4_AWARDS = ['Season IV Best Reactions', 'Season IV Most Improved Player', 'Season IV Best Guy', '*Season IV \'Pointy Award\'*']
#----Season 5 Awards Here----
PAT_SEASON5_AWARDS = ['Season V Luckiest Player', 'Season V Best Shortcuts', '*Season V Second Place Merchant*']
CHRIS_SEASON5_AWARDS = ['Season V Best Lines','Season V Choke Artist']
KEVIN_SEASON5_AWARDS = ['Season V MVP', 'Season V Best Guy','Season V Best Item User',]
DEMITRI_SEASON5_AWARDS = ['Season V Best Reactions']
JOE_SEASON5_AWARDS = ['Season V Biggest Lacker','Season V Best Bagger']
#---------Season 6 AWARDS HERE----------
PAT_SEASON6_AWARDS = ['Season VI Steamboat Ricky Award - Best Sniper','Season VI Best Bagger']
CHRIS_SEASON6_AWARDS = ['Season VI Best Lines','Season VI Best Shortcuts','Season VI Co-Biggest Lacker','*Season VI AHA Award*']
KEVIN_SEASON6_AWARDS = ['Season VI Aaron Judge Award - MVP', 'Season VI Best Items','Season VI Best Trapper','*Season VI 2016 Warriors Award*']
DEMITRI_SEASON6_AWARDS = ['Season VI Luckiest Player','Season VI Best Reactions','Season VI Co-Biggest Lacker','Season VI Best Guy','Season VI Choke Artist']
#----------Season 7 -------------
PAT_SEASON7_AWARDS = ['Season VII Steamboat Ricky Award - Best Sniper']
CHRIS_SEASON7_AWARDS = ['*UNANIMOUS* Season VII Best Lines', '*UNANIMOUS* Season VII Best Shortcuts', '*Season VII AHA Award*']
KEVIN_SEASON7_AWARDS = ['Season VII Aaron Judge Award - MVP','Season VII Best Trapper', 'Season VII Co-Choke Artist Award']
DEMITRI_SEASON7_AWARDS = ['Season VII Co-Best Guy Award','Season VII Co-Choke Artist Award']
MIKE_SEASON7_AWARDS = ['Season VII \"Must get the win, must get the win\" Award - Best Reactions', 'Season VII Rookie of the Year', 'Season VII Co-Best Guy Award','*Season VII Biggest Draft Bust*']

#----------Season 8 here -------

#-----HIGH SCORE AWARDS------
SHANE_SCORE_AWARDS = ['Perfect 120 - Nov 24th 2023']
KEVIN_SCORE_AWARDS = ['Perfect 120 - Feb 10th 2025','Scored 115: x2', 'Scored 114: x3' ,'Scored 112: x2 ','Scored 111: x2', 'Scored 110: x2']
DEMITRI_SCORE_AWARDS = ['Perfect 120 - Sept 3rd 2024','Scored 115 x1','Scored 112: x1','Scored 111: x1', 'Scored 110: x2']
PAT_SCORE_AWARDS = ['Scored 114: x2','Scored 111: x3','Scored 110: x1']
CHIRS_SCORE_AWARDS = ['Scored 111: x1','Scored 110: x1']
#-----------------

#----COMEBACK AWARDS-----
CHRIS_COMEBACK_AWARDS = ["Win GP with a 12th place: x1","Win a GP with a 6th place: x1"]

#--TPURNIMENT AWARDS--
PAT_TOURNIMENT_AWARDS = ["First Kartnite Championship (Season VI) Champion"]
DEMITRI_TOURNIMENT_AWARDS = ["Okemo Vehical Elimination Champion ", "First Kartnite Knockout Tournament Champion"]
KEVIN_TOURNIMENT_AWARDS = ["Second Kartnite Championship (Season VII) Champion"]

#--------




#A LIST OF ALL PLAYERS SEASONAL AWARDS
PAT_AWARDS = [PAT_RETRO_AWARDS,PAT_SEASON2_AWARDS,PAT_SEASON3_AWARDS,PAT_SEASON4_AWARDS,PAT_SEASON5_AWARDS,PAT_SEASON6_AWARDS,PAT_SEASON7_AWARDS]
CHRIS_AWARDS = [CHRIS_RETRO_AWARDS,CHRIS_SEASON2_AWARDS,CHRIS_SEASON3_AWARDS,CHRIS_SEASON4_AWARDS,CHRIS_SEASON5_AWARDS,CHRIS_SEASON6_AWARDS,CHRIS_SEASON7_AWARDS]
KEVIN_AWARDS = [KEVIN_RETRO_AWARDS,KEVIN_SEASON2_AWARDS,KEVIN_SEASON3_AWARDS,KEVIN_SEASON4_AWARDS,KEVIN_SEASON5_AWARDS,KEVIN_SEASON6_AWARDS,KEVIN_SEASON7_AWARDS]
DEMITRI_AWARDS = [DEMITRI_RETRO_AWARDS,DEMITRI_SEASON2_AWARDS,DEMITRI_SEASON3_AWARDS,DEMITRI_SEASON4_AWARDS,DEMITRI_SEASON5_AWARDS,DEMITRI_SEASON6_AWARDS,DEMITRI_SEASON7_AWARDS]
JOE_AWARDS = [JOE_SEASON2_AWARDS,JOE_SEASON3_AWARDS,JOE_SEASON5_AWARDS]
MIKE_AWARDS = [MIKE_SEASON7_AWARDS]
SHANE_AWARDS = []

#APPENDING THE HIGH SCORES
KEVIN_AWARDS.append(KEVIN_SCORE_AWARDS)
SHANE_AWARDS.append(SHANE_SCORE_AWARDS)
DEMITRI_AWARDS.append(DEMITRI_SCORE_AWARDS)
PAT_AWARDS.append(PAT_SCORE_AWARDS)
CHRIS_AWARDS.append(CHIRS_SCORE_AWARDS)

#append the comback awards
CHRIS_AWARDS.append(CHRIS_COMEBACK_AWARDS)

#append the tourniment awards
PAT_AWARDS.append(PAT_TOURNIMENT_AWARDS)
DEMITRI_AWARDS.append(DEMITRI_TOURNIMENT_AWARDS)
KEVIN_AWARDS.append(KEVIN_TOURNIMENT_AWARDS)





#final dictonary
AWARD_LIST = {'Pat' : PAT_AWARDS,
              'Chris' : CHRIS_AWARDS,
              'Kevin' : KEVIN_AWARDS,
              'Demitri' : DEMITRI_AWARDS,
              'Joe' : JOE_AWARDS,
              'Shane': SHANE_AWARDS,
              'Karla': [],
              'Mike' : MIKE_AWARDS,
              'Jason' : [],
              'Matt' : [],
              'John': []}

#file path extention for images
#this is needed since wkhtmltopdf needs absolute paths for functionality :(
#PATH_EXT = "C:\\Users\\patri\\Github_Directories\\Kartnite\\Kartnite_Stats\\player_profile\\"
PATH_EXT = "/home/pat/KartniteStats/Kartnite_Stats/"
