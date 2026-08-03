"""
PM

Generate all of the html files for a github site version of the time trial stats.
"""

import shutil
import sys

from constants import LIST_OF_TRACK_NAMES,LIST_OF_TRACK_NAMES_SHORTCUT
import time_trial_profile as ttp
import time_trial_stats as tts
import os

def create_index_page():
    #crete a new index.html file in the github_site folder
    with open("github_site/index.html", 'w') as f:
        f.write("<html><head><title>Kartnite Stats</title></head><body>")
        f.write("<h1>Kartnite Stats</h1>")
        f.write("<p>Welcome to the Kartnite Stats Github Site!</p>")
        f.write("<p>Here you can find the time trial stats for all tracks.</p>")
        f.write("<p>Click on a track below to view the stats:</p>")
        f.write("<ul>")
        for track in LIST_OF_TRACK_NAMES:
            f.write(f"<li><a href='tracks/{track.replace(' ','_').replace("'","")}.html'>{track}</a></li>")
        f.write("</ul>")
        f.write("</body></html>")


def main():

    #create a new directory at the top level of the project called "github_site"
    if not os.path.exists("github_site"):
        os.mkdir("github_site")   

    #inside create a subdirectory called categories
    if not os.path.exists("github_site/tracks"):
        os.mkdir("github_site/tracks")
    
    #slightly modified version of the "create_time_trial_profile" function
    
    #for output redirection later
    print('Generating All HTML Files...')
    default_stdout = sys.stdout

    #gather all data necessarry:
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}
    all_histories_nsc = {}
    #data is now in the format of: 
    #{player : {track: (time, date_set), ...}, ...}
    for playerx in players:
        all_histories[playerx] = tts.convert_history_to_dict(playerx)
        all_histories_nsc[playerx] = tts.convert_nsc_history_to_dict(playerx)


    #create the index page
    print("Generating the Index.html")
    create_index_page()


    base_filepath = "github_site/tracks/"

    for track in LIST_OF_TRACK_NAMES:
        filename = base_filepath + track.replace(" ","_").replace("'","") + ".html"
        sys.stdout = open(filename, 'w')
        ttp.htmlHeaders()

        if track in LIST_OF_TRACK_NAMES_SHORTCUT:
            ttp.create_category_page(all_histories,track,"Unrestricted", extra_txt = "")
            ttp.create_category_page(all_histories_nsc,track,"Non-Shortcut", extra_txt = "NSC")
        else:
            ttp.create_category_page(all_histories,track,"Unrestricted", extra_txt = "")


    sys.stdout = default_stdout
    print("All HTML Files Generated!")

    #copy tmp_images folder from time_trials to the github_site folder
    if not os.path.exists("github_site/tracks/record_images"):
        os.mkdir("github_site/tracks/record_images")

    for filename in os.listdir("time_trials/tmp_imgs"):
        if os.path.isfile(f"time_trials/tmp_imgs/{filename}"):
            shutil.copy(f"time_trials/tmp_imgs/{filename}", f"github_site/tracks/record_images/{filename}")

    print("All Images Copied!")


    #go through all html files and update the image src to point to the new location
    for filename in os.listdir("github_site/tracks"):
        if filename.endswith(".html"):
            filepath = f"github_site/tracks/{filename}"
            with open(filepath, 'r') as file:
                filedata = file.read()

            # Replace the old image src with the new one
            filedata = filedata.replace('src= /home/pat/KartniteStats/Kartnite_Stats/time_trials/tmp_imgs/', 'src= record_images/')

            # Write the updated content back to the file
            with open(filepath, 'w') as file:
                file.write(filedata)

    #Go through all of the html files and add a back button to the top of the page that links back to the index.html page
    for filename in os.listdir("github_site/tracks"):
        if filename.endswith(".html"):
            filepath = f"github_site/tracks/{filename}"
            with open(filepath, 'r') as file:
                filedata = file.read()

            # Add a back button to the top of the page
            back_button_html = '<a href="../index.html">Back</a><br>'
            filedata = filedata.replace('<body>', f'<body>{back_button_html}')

            # Write the updated content back to the file
            with open(filepath, 'w') as file:
                file.write(filedata)


    return 

    






if __name__ == "__main__":
    main()
   