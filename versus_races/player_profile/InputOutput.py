from Constants import *
from PlayerProfile import createPlayerProfile
from LeaderboardGenerators import *
from PlayerProfile import *
from StatGetters import *


#This file controls the main I/O Experiance for the User, it will promt the user and ask what they would like to do in regards to inputs
#viewing, or making a player profile, and then it will execute this, by calling any of the other methods in the other files as
#nessassary

#This is the main bulk of the code, it culminates all of the previous functions 
#into the user inputted choices, this is the method that gets user inputs and does all 
#of the database scraping and saving for this program to work.
def RunKartniteStats(version, contributors):
### Patrick Marinich December 2021

  #constants
  VERSION_NUMBER = version
  CONTRIBUTORS = contributors

  #Below is the logic for asking a user what they would like to do
  ########


  #displaying inputs for the user
  print('Welcome to Kartnite Stats ' ,VERSION_NUMBER , "\nDeveloped by:", CONTRIBUTORS, '\n')
  print('Below are the options, type the number of the option you would like')
  print('1. Email A Player Profile\n')
 
  selection = input('What Would You Like To Do: ')
  
  #Generate the PDF for the player or players
  if selection == '1':
    #generates a pdf profile of the inputted players stats for viewing pleasure
    print('Generate a player Report below by entering their name, and your email infromation')
    players = input('Player Name: ')
    email = input('Enter Your Email:')
    password = input('Password: ')
    message = input('Message for the email:')

    #allows for all players (who are interested) reports to be generated at once
    if players == 'all' or players == 'All' or players == 'ALL':
      racers = ['Pat', 'Kevin', 'Demitri', 'Chris', 'Joe','Shane','Mike', 'Danny']
      for player in racers:
        HTML = createPlayerProfile(player,TRACK_INDEX)
        generatedFile,events = convertHTMLtoPDF(HTML)
        sendReport(player,email,password,message,generatedFile,events)
    else:
        player = players
        HTML = createPlayerProfile(player,TRACK_INDEX)
        generatedFile,events = convertHTMLtoPDF(HTML)
        sendReport(player,email,password,message,generatedFile,events)
  else: 
    print('invalid selection restart the program')






