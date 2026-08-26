#Patrick Marinich

#Now that I have been improving my coding abilities due to working full time, I want to try and take on the task of automating putting the stats in, updating the database 
#and sending out the stats perodically.
#At a minimum I will need a parser which can convert the text file that I write while playing and convert it into a usable input form, so that is the goal of this file

import re

from player_profile.Constants import PLAYERS,PLAYERS_INIT,TRACK_NICKNAMES

#take in a text file, return the infromation from it.
def parse_input(file):
    
    #I will assume that the file is made up of lines in the format of:
    # track player1 player2 player3 player4? extra stats.....
    # track ....
    # track ....
    # ....
    # player win <number>

    #the lines with the track are the individual races, the player win determines the GP Winner
    #extra stats include the blue shells and shocks

    #Successful Parse Data
    data = []
    #error list
    errors = []
    #info list
    info = []

    line_count = 0
    for line in file:

        #for error tracking
        line_count += 1
        #if the line is just a newline skip
        if line == '\n':
            continue

        

        #remove any dots
        line = line.replace(".","")
        #standardize
        line = line.upper()
        #remove extra spaces
        line = line.rstrip()
        line = line.replace("\n","")
        #split along the spaces
        arr = line.split(" ")

        #remove extra spaces
        for i in range(0,len(arr)):
            arr[i] = arr[i].rstrip()
            arr[i] = arr[i].replace('\n','')
        if "" in arr:
            arr.remove("")
        
        #if empty arr, then skip.
        if arr == [] or arr == None:
            continue

        #print(arr)
        #check if arr can grab out the data.
        # No matches we will continue and play it off as info
        # if there is a partial match then we will throw errors

        #Check if doing a GP WIN:
        if "WIN" in arr:
            #if win is the last thing swap it with the score
            if arr[2] == "WIN":
                temp = arr[2]
                arr[2] = arr[1]
                arr[1] = temp

            #attempt to match with a player, if so pass if fail throw error
            if arr[0] not in PLAYERS:
                errors.append(("ERROR GP WIN | PLAYER DOES NOT EXIST",line_count))
            else:
                #check score is valid
                if int(arr[2]) > 120:
                    errors.append(("ERROR GP WIN | SCORE IMPOSSIBLE",line_count))
                
                #if so then good to go
                data.append(("GPWIN",arr[0].replace('\n',""),arr[2].replace('\n',"")))
                continue
        else:
            
            #check if the first elem is a track
            if arr[0] in TRACK_NICKNAMES.keys():
                
                #we have a track, now check if we have valid players
                #there will be 3 or 4 players listed with maybe a number in it
                players_scores = []
                for i in range(0,3):
                    #match with regex
                    p = re.search("([A-Z]+)([0-9]*)",arr[i+1])
                    #print(p)
                    if p != None:
                        #we found player
                        if p.group(1) in PLAYERS_INIT:
                            players_scores.append([p.group(1),p.group(2)])
                        else:
                            errors.append(("INITIAL " + p.group(1)+ " NOT IN LIST ",line_count))
                    else:
                        #player formatted wrong
                        errors.append(("PLAYER " + str(i+1) + " NOT FORMATTED PROPERLY",line_count))
                
                

                #there may be a forth player at location 5. if there is do above, if not then it falls into the "extra stats bucket"
                p = None
                if len(arr) > 4:
                    p = re.search("([A-Z]+)([0-9]*)",arr[4])
                    if p != None:
                        if p.group(1) in PLAYERS_INIT:
                            players_scores.append([p.group(1),p.group(2)])
                        else:
                            p = None
                
                #then check the rest for extra stats
                extras = []
                start_idx = 5 if p != None else 4

                #go through the rest of the arr, look for stats
                curr_state = 0
                curr_player = ""
                curr_count = ""
                for i in range(start_idx,len(arr)):
                    #if state is 0 we expect a name
                    #if state is 1 we expect EITHER a number or BLUE,SHOCK,DODGE
                    #if state is 2 we expect BLUE,SHOCK,DODGE
                    
                    #make KEV -> KEVIN
                    if curr_player == 'KEV':
                        curr_player = "KEVIN"

                    if curr_state == 0:
                        #epxecting player
                        if arr[i] in PLAYERS:
                            curr_state = 1
                            curr_player = arr[i]
                        else:
                            errors.append(("STATE EXPECTED PLAYER GOT " + arr[i],line_count))
                    elif curr_state == 1:
                        #check if number
                        #check if TYPE
                        n = re.search("[0-9]+",arr[i])
                        if n != None:
                            #got a number
                            curr_count = arr[i]
                            curr_state = 2
                        elif arr[i] in ["SHOCK","BLUE","DODGE"]:
                            #end of an extra
                            extras.append((arr[i],1,curr_player))
                            curr_state = 0
                        else:
                            errors.append(("STATE EXPECTED TYPE OR NUMBER GOT " + arr[i],line_count))
                    elif curr_state == 2:
                        #expecting type
                        if arr[i] in ["SHOCK","BLUE","DODGE"]:
                            #end of an extra
                            extras.append((arr[i],curr_count,curr_player))
                            curr_state = 0
                        else: 
                            errors.append(("STATE EXPECTED TYPE GOT " + arr[i],line_count))
                    else:
                        errors.append(("STATE INFROMATION IN EXTRAS GOT MESSED UP",line_count))
                
                #at the end of the loop the state should be 0, if not throw error
                if curr_state != 0:
                    errors.append(("STATE DID NOT END AT 0", line_count))


                #go through, and append the data
                #(TRACK,racer,score,racer,score,racer,score,racer,score)
                #(TYPE,COUNT,PLAYER)
                placement_scores = {1:15,2:12,3:10,4:8,5:7,6:6,7:5,8:4,9:3,10:2,11:1,12:0}
                c = 1
                for i in range(0,len(players_scores)):
                    #include the placements if there are not any
                    if players_scores[i][1] == None or players_scores[i][1] == "":
                        players_scores[i][1] = c
                    c +=1
                #convert to the score
                for i in range(0,len(players_scores)):
                    players_scores[i][1] = placement_scores[int(players_scores[i][1])]
                
                #append to data
                #print(players_scores)
                if len(players_scores) == 3:
                    data.append((arr[0],players_scores[0][0],players_scores[0][1],players_scores[1][0],players_scores[1][1],players_scores[2][0],players_scores[2][1]))
                else:
                    data.append((arr[0],players_scores[0][0],players_scores[0][1],players_scores[1][0],players_scores[1][1],players_scores[2][0],players_scores[2][1],players_scores[3][0],players_scores[3][1]))

                for elem in extras:
                    data.append(elem)



            else:
                
                #check if its 3 or 4 letters, and not a player name, if so then its probably a typo so add error
                if (len(arr[0]) == 3 or len(arr[0]) == 4) and arr[0] not in PLAYERS and arr[0] != "KART":
                    errors.append(("POSSIBLE TRACK TYPO", line_count))
                else:
                    #then we have a line of nothing, not a track or 
                    info.append(line)

    return data,errors,info


#main for testing
if __name__ == "__main__":
    f = open('C:\\Users\\patri\\Github_Directories\\Kartnite\\auto_input\\current_inputs.txt','r')

    data,errors,info = parse_input(f)
    print(data)
    print(errors)
    print(info)

