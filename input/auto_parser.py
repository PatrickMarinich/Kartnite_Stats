#Patrick Marinich

#Now that I have been improving my coding abilities due to working full time, I want to try and take on the task of automating putting the stats in, updating the database 
#and sending out the stats perodically.
#At a minimum I will need a parser which can convert the text file that I write while playing and convert it into a usable input form, so that is the goal of this file

import re

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

    #STD INFO
    PLAYERS = ["PAT","DEMITRI","KEVIN","KEV","CHRIS","JOE","SHANE","MIKE","MATT","JASON","KARLA","CALLUM","JOHN","DANNY","HENRY"]
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
        "DA" : "Danny",
        "H": "Henry"
    }
    TRACKS = {"Luigi":"Luigi Circuit",
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
            if arr[0] in TRACKS.keys():
                
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

