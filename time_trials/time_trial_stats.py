#June 2025

#This file will be responsible for generating stats for the pdf, the email will be done in another file
import datetime
from datetime import datetime
from datetime import date,timedelta
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

PLAYER_COLORS = {"Pat": 'darkorange', "Demitri": 'green', "Chris": "magenta", "Kevin": 'royalblue', 'Mike': 'purple', "John": '#98E1D0'}
PATH_EXT = "/home/pat/KartniteStats/Kartnite_Stats/"

#open up the history file and create a dict with all of the tracks, the PR set and what date it was set on
def convert_history_to_dict(player):
    #open file
    history_file = open(PATH_EXT+"time_trials/player_data/shortcut/"+player+"_history.csv", "r")
    format_string_date = "%m/%d/%Y"
    format_string_time = "%M:%S.%f" 

    #add in the form track: (race time, date)
    history = {}
    for line in history_file:
        line = line.replace("\n","") #remove endline
        data = line.split(",")  #split csv

        if data[0] in history.keys():
            history[data[0]].append((datetime.strptime(data[1],format_string_time),datetime.strptime(data[2],format_string_date)))
        else:
            history[data[0]] = [(datetime.strptime(data[1],format_string_time),datetime.strptime(data[2],format_string_date))]
    
    return history

#Identical to above, but using the non-shortcut times
def convert_nsc_history_to_dict(player):
    #open file
    history_file = open(PATH_EXT+"time_trials/player_data/non_shortcut/"+player+"_history.csv", "r")
    format_string_date = "%m/%d/%Y"
    format_string_time = "%M:%S.%f" 

    #add in the form track: (race time, date)
    history = {}
    for line in history_file:
        line = line.replace("\n","") #remove endline
        data = line.split(",")  #split csv

        if data[0] in history.keys():
            history[data[0]].append((datetime.strptime(data[1],format_string_time),datetime.strptime(data[2],format_string_date)))
        else:
            history[data[0]] = [(datetime.strptime(data[1],format_string_time),datetime.strptime(data[2],format_string_date))]
    
    return history

#generate the current leaderboard of everybodys PRs for a given track (their most recent times)
def get_current_leaderboard(all_histories,track):
    
    #iterate through all items
    data = []
    format_string_time = "%M:%S.%f" 
    format_string_date = "%m/%d/%Y"
    #name,time,date
    for k,v in all_histories.items():
        if v != {}:
            if track in v.keys():
                data.append([k,datetime.time(v[track][len(v[track])-1][0]),datetime.date(v[track][len(v[track])-1][1])])
            else: 
                data.append([k,(datetime.time(datetime.strptime("09:59.999",format_string_time))),datetime.date(datetime.strptime("12/31/9999",format_string_date))])
        else:
            data.append([k,(datetime.time(datetime.strptime("09:59.999",format_string_time))),datetime.date(datetime.strptime("12/31/9999",format_string_date))])
    
    #create the dataframe
    df = pd.DataFrame(data,columns=['Name','Time','Date'])
    df = df.sort_values(by="Time")

    def format_time(x,format_string_time):
        return x.strftime(format_string_time)[:-3]
    def format_date(x):
        vals = str(x).split("-")
        return vals[1]+"/"+vals[2]+"/"+vals[0]
        

    #format times/dates nicely
    df['Time'] = df['Time'].apply(lambda x: format_time(x, format_string_time))
    df['Date'] = df['Date'].apply(lambda x: format_date(x))
    return df



#generate a line plot of all of the players times over time on the track, since june 1st 2025
#data of the form time,date
def get_players_line_graph(all_histories,track,extra_txt = ""):
    
    #iterate through the items:
    players = []
    data = [] #list of lists
    i = 0
    for k,v in all_histories.items():
        players.append(k)
        if v != {}:
            if track in v.keys():
                data.append(v[track])
            else:
                data.append([])
        else:
            data.append([])
    
    #data is in player order, so plot that way
    #create a new figure object for this graph
    plt.figure()
    for i in range(len(players)):
        
        #for each set of points, unzip into a list of times and dates
        unzipped_list =  list(map(list, zip(*data[i])))
        if unzipped_list != []:      
            #set any dates before june 1st 2025 to this date
            j = 0
            DEFAULT_DATE = datetime(2025, 6, 1, 0, 0, 0) 
            for x in unzipped_list[1]:
                if x < DEFAULT_DATE:
                    unzipped_list[1][j] = DEFAULT_DATE
                j = j + 1  

            if date.today() not in unzipped_list[1]:
                #Include an additional point for todays date and the previous time if not set today
                unzipped_list[1].append(date.today())
                unzipped_list[0].append(unzipped_list[0][-1]) #reappend the last elem
            
            #formatting datetime objects
            def format_time(x,pos=None):

                dt = mdates.num2date(x)
                format_string_time = "%M:%S.%f" 
                label = dt.strftime(format_string_time)
                return label[:-3]
            def format_date(x,pos=None):
                print(x)
                vals = str(x).split("-")
                return vals[1]+"/"+vals[2]+"/"+vals[0]
            
            y_formatter = FuncFormatter(format_time)
            x_formatter = FuncFormatter(format_date)
            plt.gca().yaxis.set_major_formatter(y_formatter)
            plt.plot(unzipped_list[1],unzipped_list[0],label=players[i],color=PLAYER_COLORS[players[i]],linewidth=1,drawstyle='steps-post')

    plt.legend()
    plt.title("Player History")
    name = 'time_trials/tmp_imgs/'+track.replace(" ","").replace("'","")+'_history'+ extra_txt + '.png'

    plt.savefig(name)
    plt.close() 
    return name

#each day that passes, the player with the best time gets X points, second best Y points, third best Z points, june first 2025
def get_time_trial_scores(all_histories,track):
    
    FIRST_POINTS = 1
    SECOND_POINTS = 0.2
    THIRD_POINTS = 0.04

    #TT stats started on june 1st 2025
    start_date = datetime(2025, 6, 1)
    end_date = datetime.today()

    #time step is one day 
    d = timedelta(days=1)

    #init the scores dict
    track_scores = {}
    curr_times = {}
    for k in all_histories.keys():
        track_scores[k] = 0
        curr_times[k] = datetime(1900, 1, 1, 0, 9, 59, 999000)

    #iterate over each day
    #Store the best time per player up to this date
    #then look at the top 3 and add their points
    all_histories_cpy = deepcopy(all_histories)
    while (start_date <= end_date):
    
        #for each player
        for k in all_histories_cpy.keys():
            if track in all_histories_cpy[k].keys():
                if all_histories_cpy[k][track]!= []: 
                    while(all_histories_cpy[k][track][0][1] <= start_date): #doing this in a loop should take care of mapping any pre- 06/01/25 times

                        curr_times[k] = all_histories_cpy[k][track][0][0]
                        all_histories_cpy[k][track].pop(0)

                        if all_histories_cpy[k][track] == []:
                            break

        #convert hashmap to a list of lists. sort by time
        day_list = []
        for k,v in curr_times.items():
            day_list.append([k,v])
        day_list.sort(key=lambda x: x[1])
        #print(day_list)

        #increment points to the top 3
        track_scores[day_list[0][0]] += FIRST_POINTS
        track_scores[day_list[1][0]] += SECOND_POINTS
        track_scores[day_list[2][0]] += THIRD_POINTS
        
        #round trackscores to prevent floating point errors (3 decimal places)
        track_scores[day_list[0][0]] = round(track_scores[day_list[0][0]],3)
        track_scores[day_list[1][0]] = round(track_scores[day_list[1][0]],3)
        track_scores[day_list[2][0]] = round(track_scores[day_list[2][0]],3)
        
        #move to the next day
        start_date += d

    data = []
    for k,v in track_scores.items():
        data.append([k,v])
    return pd.DataFrame(data,columns=["Player","Track Score"]).sort_values(by="Track Score", ascending=False)


#iterate through all of the days and count who has the best time, make a pie chart
def get_pie_chart_days_in_first(all_histories,track,extra_txt = ""):
    
    #TT stats started on june 1st 2025
    start_date = datetime(2025, 6, 1)
    end_date = datetime.today()

    #time step is one day 
    d = timedelta(days=1)

    #init the scores dict
    days_in_first = {}
    curr_times = {}
    for k in all_histories.keys():
        days_in_first[k] = 0
        curr_times[k] = datetime(1900, 1, 1, 0, 9, 59, 999000)

    #iterate over each day
    #Store the best time per player up to this date
    #then look at the top 3 and add their points
    all_histories_cpy = deepcopy(all_histories)
    while (start_date <= end_date):
    
        #for each player
        for k in all_histories_cpy.keys():
            if track in all_histories_cpy[k].keys():
                if all_histories_cpy[k][track]!= []: 
                    while(all_histories_cpy[k][track][0][1] <= start_date): #doing this in a loop should take care of mapping any pre- 06/01/25 times

                        curr_times[k] = all_histories_cpy[k][track][0][0]
                        all_histories_cpy[k][track].pop(0)

                        if all_histories_cpy[k][track] == []:
                            break

        #convert hashmap to a list of lists. sort by time
        day_list = []
        for k,v in curr_times.items():
            day_list.append([k,v])
        day_list.sort(key=lambda x: x[1])

        #increment increment the player in first by 1
        days_in_first[day_list[0][0]] += 1
        
        #move to the next day
        start_date += d

    #make a list, remove any players with 0 days
    names = []
    days = []
    for k,v in days_in_first.items():
        if v != 0:
            names.append(k)
            days.append(v)

    #custom labeling
    total = sum(days)
    def autopct_format(pct):
        val = int(round(pct * total / 100.0))
        return f'{val}\n({pct:.1f}%)'

    #match player to color
    colors = list(map(lambda x: PLAYER_COLORS[x], names))

    #plt.figure()
    fig, ax = plt.subplots()
    ax.pie(days, labels=names, autopct=autopct_format,colors=colors)
    plt.title("Days in First Place")
    #plt.show()

    name = 'time_trials/tmp_imgs/'+track.replace(" ","").replace("'","")+'_pie' + extra_txt + '.png'

    plt.savefig(name,bbox_inches='tight')
    plt.close() 
    return name

#get a graph of the overall #1 times over time. Color by player
def get_record_line(all_histories, track, extra_txt = ""):
    #TT stats started on june 1st 2025
    start_date = datetime(2025, 6, 1)
    end_date = datetime.today()

    #time step is one day 
    d = timedelta(days=1)

    #init the scores dict
    curr_times = {}
    for k in all_histories.keys():
        curr_times[k] = datetime(1900, 1, 1, 0, 9, 59, 999000)

    #iterate over each day
    #Store the best time per player up to this date
    all_histories_cpy = deepcopy(all_histories)
    first_place = []
    while (start_date <= end_date):
    
        #for each player
        for k in all_histories_cpy.keys():
            if track in all_histories_cpy[k].keys():
                if all_histories_cpy[k][track]!= []: 
                    while(all_histories_cpy[k][track][0][1] <= start_date): #doing this in a loop should take care of mapping any pre- 06/01/25 times

                        curr_times[k] = all_histories_cpy[k][track][0][0]
                        all_histories_cpy[k][track].pop(0)

                        if all_histories_cpy[k][track] == []:
                            break

        #convert hashmap to a list of lists. sort by time
        day_list = []
        for k,v in curr_times.items():
            day_list.append([k,v])
        day_list.sort(key=lambda x: x[1])

        #whoever is in first, list the name, time date
        first_place.append([day_list[0][0],day_list[0][1],start_date])
        
        #move to the next day
        start_date += d

    #print(first_place)

    #formatting datetime objects
    def format_time(x,pos=None):
        dt = mdates.num2date(x)
        format_string_time = "%M:%S.%f" 
        label = dt.strftime(format_string_time)
        #print(dt, label)
        return label[:-3]
    def format_date(x,pos=None):
        print(x)
        vals = str(x).split("-")
        return vals[1]+"/"+vals[2]+"/"+vals[0]
    
    #all of the dates
    x = [x[2] for x  in first_place]
    #all of the times
    y = [y[1] for y in first_place]
    #for coloring the line
    names = [z[0] for z in first_place]

    #a new line is plotted each time there is a new name in the list.
    prev_name = None
    curr_x = []
    curr_y = []
    i = 0
    names_used = []
    #plot a point at the very first time, if there is only one time then the axis is broken, plotting a point seems to fix it
    plt.plot(x[0],y[0] + timedelta(milliseconds=1),label="_nolegend_")
    for name in names: 
        #same person held record, so add day to list
        if prev_name == name:
            curr_x.append(x[i])
            curr_y.append(y[i])  
        #very first elem, log dont plot
        elif prev_name == None:
            curr_x = [x[i]]
            curr_y = [y[i]]
        else:
            #different person, so clear plot an clear x & y
            label = prev_name
            if prev_name in names_used:
                label = "_nolegend_"
            plt.plot(curr_x,curr_y,color = PLAYER_COLORS[prev_name],label=label,drawstyle='steps-pre')
            names_used.append(prev_name)
            #include prev point so the lines connect
            curr_x = [x[i-1],x[i]]
            curr_y = [y[i-1],y[i]]

        prev_name = name
        i += 1
    
    #when complete plot the last segment
    #print(curr_y)
    label = prev_name
    if prev_name in names_used:
        label = "_nolegend_"
    plt.plot(curr_x,curr_y,color = PLAYER_COLORS[prev_name],label=label,drawstyle='steps-pre')

    y_formatter = FuncFormatter(format_time)
    x_formatter = FuncFormatter(format_date)
    plt.gca().yaxis.set_major_formatter(y_formatter)
    plt.title("Kartnite Record")
    plt.legend()
    #plt.show()

    name = 'time_trials/tmp_imgs/'+track.replace(" ","").replace("'","")+'_recordline' + extra_txt + '.png'

    plt.savefig(name)
    plt.close() 
    return name

#find the longest lasting record for a track, and the length of the current time, since june 1st 2025
def get_time_record_was_held(all_histories,track):
   pass #not yet implemented



if __name__ == "__main__":
    players= ["Pat","Kevin","Chris","Demitri","John","Mike"]
    all_histories = {}

    #data is now in the format of: 
    #{player : {track: (time, date_set), ...}, ...}
    for player in players:
        all_histories[player] = convert_history_to_dict(player)

    #print(all_histories)
    #print(get_current_leaderboard(all_histories,'GCN DK Mountain'))
    #print(get_current_leaderboard(all_histories,'DS Desert Hills'))

    #get_players_line_graph(all_histories,'GCN DK Mountain')

    #track_scores = get_time_trail_scores(all_histories,"GCN DK Mountain")
    #print(track_scores)
    #track_scores = get_time_trail_scores(all_histories,"Rainbow Road")
    #print(track_scores)
    #get_pie_chart_days_in_first(all_histories,"Moo Moo Meadows")
    get_record_line(all_histories,"Moo Moo Meadows")