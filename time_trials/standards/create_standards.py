#PM July 2025 
#The goal of this script is to take in the player standards from the player pages website and make python dictonaries out of them.
#With the goal to be to be able to use them for other parts of the project 

#The idea:
#Copy paste the 3 tables into 3 seperate files directly from the website
#remove the FLAP (fast lap) times 
#remove any unneeded text
#convert times into the format MM:SS.mmm
#print legal python code

#initially these files will be of the form
# ranks
# points
# track times
# FLAP times

#gather rank names from the first line
#points can be skipped
#get track time->rank pair
#FLAP times can be skipped

import sys

#include constants file
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import *

def parse_standards_text_file(file1,ranks,times):
    firstline = 0
    for line in file1:

        #get line into a list of words
        line_split = line.split("\t")

        #get the rank names
        if firstline == 0:
            for word in line_split:
                if word != "Std:":
                    ranks.append(word.strip())
            firstline = 1
        else: 
            #if the line starts with 'flag' then its a FLAP, otherwise its a 3lap
            if line_split[0] != "flag" and line_split[0] != "Pts:":
                if line_split[0] not in times.keys():
                    times[line_split[0]] = []
                #add all the times to the list
                for i in range(1,len(line_split)):
                    if line_split[i].strip() != "flag":

                        #convert the time from m'ss"mm?m? to MM:SS.mmm
                        curr_time = line_split[i].strip()
                        new_time = ""
                        if curr_time == "*":
                            #max time for unplayed tracks is being counted as 09:59.999
                            new_time = "10:00.000"
                        else:
                            #minutes
                            if "\'" in curr_time:
                                new_time += "0" + curr_time[0] + ":"
                                #remove those characters
                                curr_time = curr_time[2:]
                            else:
                                new_time += "00:"
                            
                            #seconds (next 2 chars)
                            new_time += curr_time[0] + curr_time[1] + "."
                            #remove those characters and the ""
                            curr_time = curr_time[3:]
                            
                            #milliseconds, we are either left with 1,2,3 values
                            #if less than 3 append 0s
                            while len(curr_time) < 3:
                                curr_time += "0"
                            
                            new_time += curr_time
                            #add the updated formatted time to the list
                        times[line_split[0]].append(new_time)
    return ranks, times


#this function will be to take in the array of rank names as well as all of the times and convert it into legal python syntax so that
#it can be used in another part of the project.
#output structure
#NAME = {rank : time, rank: time}....
#returns an array of the names used for later use

def convert_standards_to_dict(ranks,times,var_name_ext):

    dictionary_names = []
    #for each track create a new string that will be a python dictonary
    for track in times.keys():
        curr_str = track + "_"+var_name_ext+ " = {"

        #for each rank get the time
        for i in range(len(ranks)):
            curr_str += '"'+ ranks[i] + "\" : \"" + times[track][i] + '"'
            #if not at the end include comma and new line
            if i != len(ranks) - 1:
                curr_str+= ",\n"
        #end the dict, and print
        curr_str += '}'
        print(curr_str)
        dictionary_names.append(str(track + "_"+var_name_ext))

    #return a list of the track names
    return dictionary_names

#given the 2D array of lists, create a dictionary with the track's name as the key and the value being a len 2 array with the SC standards and the NCS standards
def create_name_mapping(names):
    ret = {}
    i = 0
    for track in LIST_OF_TRACK_NAMES:
        ret[track] = [names[1][i],names[0][i]]
        i += 1

    #print in a usable format, just remove last comma before using in another file
    print("TRACK_TO_STANDARDS = {")
    for k,v in ret.items():
        print("\""+ k + "\" : [" + v[0] + "," + v[1] + "],")
    print('}')


if __name__ == "__main__":
    f_out = open("tmp_out.txt", 'w')
    sys.stdout = f_out
    #open up the 3 nsc files
    file1 = open("time_trials/standards/nsc1.txt",'r')
    file2 = open("time_trials/standards/nsc2.txt",'r')
    file3 = open("time_trials/standards/nsc3.txt",'r')
    ranks = []
    times = {}
    #get the data from them
    ranks,times = parse_standards_text_file(file1,ranks,times)
    ranks,times = parse_standards_text_file(file2,ranks,times)
    ranks,times = parse_standards_text_file(file3,ranks,times)

    names = []
    #convert to legal python
    ret = convert_standards_to_dict(ranks,times,var_name_ext="non_shortcut_standards")
    names.append(ret)
    #now do the same for the shortcut standards
    file1 = open("time_trials/standards/sc1.txt",'r')
    file2 = open("time_trials/standards/sc2.txt",'r')
    file3 = open("time_trials/standards/sc3.txt",'r')
    ranks = []
    times = {}
    #get the data from them
    ranks,times = parse_standards_text_file(file1,ranks,times)
    ranks,times = parse_standards_text_file(file2,ranks,times)
    ranks,times = parse_standards_text_file(file3,ranks,times)
    #convert to legal python
    ret = convert_standards_to_dict(ranks,times,var_name_ext="shortcut_standards")
    names.append(ret)

    create_name_mapping(names)
