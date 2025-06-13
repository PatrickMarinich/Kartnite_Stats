#June 2025
import time
import pdfkit
import yagmail
import os

import sys
from IPython import display
import pdfkit
from datetime import date
from copy import deepcopy
from pypdf import PdfWriter

from time_trial_stats import *

def create_time_trial_profile(player):
    #for output redirection later
    print('Generating HTML File...')
    default_stdout = sys.stdout


    #gather all data necessarry:
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}
    #data is now in the format of: 
    #{player : {track: (time, date_set), ...}, ...}
    for player in players:
        all_histories[player] = convert_history_to_dict(player)


    #HTML File name and redirecting output
    filename = player + '.html'
    #ANY PRINT OUTS BELOW THIS WILL BE IN THE HTML CODE
    sys.stdout = open(filename, 'w')

    htmlHeaders()

    create_cup_page(all_histories,"Luigi Circuit","Moo Moo Meadows","Mushroom Gorge","Toad's Factory","Mushroom Cup")
    create_cup_page(all_histories,"Mario Circuit","Coconut Mall","DK's Snowboard Cross","Wario's Gold Mine","Flower Cup")
    create_cup_page(all_histories,"Daisy Circuit","Koopa Cape","Maple Treeway","Grumble Volcano","Star Cup")
    create_cup_page(all_histories,"Dry Dry Ruins","Moonview Highway","Bowser's Castle","Rainbow Road","Special Cup")
    create_cup_page(all_histories,"GCN Peach Beach","DS Yoshi Falls","SNES Ghost Valley 2","N64 Mario Raceway","Shell Cup")
    create_cup_page(all_histories,"N64 Sherbet Land","GBA Shy Guy Beach","DS Delfino Square","GCN Waluigi Stadium","Banana Cup")
    create_cup_page(all_histories,"DS Desert Hills","GBA Bowser Castle 3","N64 DK's Jungle Parkway","GCN Mario Circuit","Leaf Cup")
    create_cup_page(all_histories,"SNES Mario Circuit 3","DS Peach Gardens","GCN DK Mountain","N64 Bowser's Castle","Lightning Cup")

    #----------Setting Output back to console--------
    sys.stdout = default_stdout
    print('Generation Complete')
    return filename


def htmlHeaders():
  #file headers
  print('<!DOCTYPE html>')
  print('<html>')
  print('<body>')
  #divs for text
  print('<style> div.center {text-align: center; } </style>')
  print('<style> div.bar { display: flex; align-items: center; width: 100%; height: 3px; background-color: #1faadb; padding: 4px;} </style>')
  print('<style> div.block { display: inline-block; padding: 3px} </style>')
  print('<style> div.trackbox {text-align: left; display: inline-block; align-items:left; width: 47%; height: 40%; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')
  print('<style> div.dfbox {text-align: left; display: inline-block; align-items:center; width: 100%; border: 0px solid black; padding: 0px; margin: auto; vertical-align: top;} </style>')

def create_track_box(all_histories, track):
    #outer box for the track
    print("<div class=\"trackbox\">")
    print("<div class=\"center\">")
    print('<h2>', track, '</h2>')
    print("</div>")

    #get the current leaderboards
    print('<div class =\"dfbox\">')
    
    curr_times = get_current_leaderboard(all_histories,track)
    print("<center>")
    print('<div class =\"block\">')
    print(curr_times.to_html(index=False,justify='left'))
    print("</div>")

    #getting the track scores
    curr_scores = get_time_trail_scores(all_histories,track)
    print('<div class =\"block\">')
    print(curr_scores.to_html(index=False,justify='right'))
    print("</div>")
    print("</center>")
    print("</div>")

    #get the current graph
     #center the graph
    print('<div class =\"center\">')
    #get the embedded HTML for the plot
    path = get_players_line_graph(all_histories,track)
    
    print('<img src=', PATH_EXT+path, 'alt=\"'+track+'\" width=\"400\" height=\"325\">' )
    print('</div>')

    print("</div>") #end of box


def create_cup_page(all_histories,track1,track2,track3,track4,cup_name):
    #title
    print("<div class=\"center\">")
    print('<h1>',cup_name, '</h1>')
    print('</div>')

    #break line
    print('<div class = \"bar\"> </div>')

    print("<center>")
    create_track_box(all_histories, track1)
    create_track_box(all_histories, track2)
    create_track_box(all_histories, track3)
    create_track_box(all_histories, track4)
    print("</center>")

def convertHTMLtoPDF(filename):
    print('Converting to PDF...')
    path = '/usr/local/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path)

    # Returns the date for file name
    today = date.today()
    today = date.isoformat(today)

    #open the file
    currFile = open(filename, 'r')
    
    #Convert
    output = 'Kartnite TT Stats - ' + today + '.pdf'
    pdfkit.from_file(currFile, output_path=output, configuration=config,options={"enable-local-file-access": "",'--keep-relative-links': ''},verbose=True)
    print('Conversion Complete...')

    #make two pdfs, one for the stats, one for the events
    merger = PdfWriter()
    merger.append("time_trials/pre_made_pdf/Kartnite TT Sheet.pdf")
    merger.append(output)
    merger.write('Kartnite TT Stats - ' + today + '.pdf')
    merger.close()

    return output


def decode(word,shift):
    txt = ""
    for letter in word:
        if letter == '.' or letter == '@' or letter in ['1','2','3','4','5','6','7','8','9','0']:
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
    emails = {'Pat' : 'grkiztb.drizezty@xdrzc.tfd',
    'Kevin' : 'bvmzewiretzjai@xdrzc.tfd',
    'Chris' : 'tyizjgrlcuirxfev@xdrzc.tfd',
    'Demitri' : 'uwfireu20@xdrzc.tfd',
    'Mike':'udzbv1228@xdrzc.tfd',
    'John':'adnlcww.22@xdrzc.tfd'}
    #the user inputs their email infromation, to send the email
    user = yagmail.SMTP(user=userEmail, password=userPass)

    # Returns the date for file name
    today = date.today()
    today = date.isoformat(today)

    #uses the dictionary to get the email for the reciepient
    user.send(to=decode(emails[player],17), subject=('Kartnite Stats from: ' +  today), contents=message,attachments = [pdfFile])

    print('Report Delievered To ', player, '!')
