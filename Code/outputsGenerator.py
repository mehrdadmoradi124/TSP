'''
This function creates the outputs for each of the files
'''

import os
import csv
from time import time as t

createFiles = True
#can flag off if files already exist. Make this False and pull in the data from the outputs folder 
#to save a lot of time

timeLimit = 5 
 # in seconds

city_list = [
    "Atlanta.tsp", "Champaign.tsp", "NYC.tsp", "SanFrancisco.tsp", "UMissouri.tsp",
    "Berlin.tsp", "Cincinnati.tsp", "Philadelphia.tsp", "Toronto.tsp",
    "Boston.tsp", "Denver.tsp", "Roanoke.tsp", "UKansasState.tsp"
]


CSVData = [
    ["Dataset", "Time(s) - BF", "Sol.Quality - BF", "Full Tour - BF", "RelError - BF",
     "Time(s) - Approx", "Sol.Quality - Approx ", "RelError - Approx",
     "Time(s) - LS", "Sol.Quality - LS "]
]

csv_file = 'results.csv'

def getQuality(filename):
    try:
        # Open the file and read the second line
        with open(filename, 'r') as file:
            second_line = file.readlines()[0].strip()
            return second_line
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except IndexError:
        print("The file does not have a second line.")

#------------- code begins here

for city in city_list:
    #BF======================================================================
    CSVEntry = [city, str(timeLimit)]
    BFcommand = "python3 tsp.py -inst " + city + " -alg BF -time " + str(timeLimit) + " -seed 0"
    if createFiles:
        try:
            os.system(BFcommand)
        except Exception as e:
            print(f"Error: {e}")
    BFfileName = city[:-4] + "_" + "BF" + "_" + str(timeLimit) + ".sol"
    score = getQuality(BFfileName)
    CSVEntry.append(score) # "Sol.Quality - BF
    CSVEntry.append("Yes") # full tour
    CSVEntry.append("TBD") # full tour
    #Approx======================================================================
    now = t()
    Approxcommand = "python3 tsp.py -inst " + city + " -alg Approx -time " + str(timeLimit) + " -seed 0"
    if createFiles:
        try:
            os.system(Approxcommand)
        except Exception as e:
            print(f"Error: {e}")
    ApproxfileName = city[:-4] + "_" + "Approx" + "_" + "0" + ".sol"
    timePassed = t() - now
    CSVEntry.append(timePassed) #Time(s) - Approx
    score = getQuality(ApproxfileName) 
    CSVEntry.append(score) # "Sol.Quality - Approx
    CSVEntry.append("TBD") # "RelError - Aprox"
    #LST===================================================================
    quality = 0
    for seed in range(10):
        LScommand = "python3 tsp.py -inst " + city + " -alg LS -time " + str(timeLimit) + " -seed " + str(seed)
        if createFiles:
            try:
                os.system(LScommand)
            except Exception as e:
                print(f"Error: {e}")
        LSfileName = city[:-4] + "_" + "LS" + "_" + str(timeLimit) + "_" + str(seed) + ".sol"
        quality += int(getQuality(LSfileName))
    avgQuality = quality / 10
    CSVEntry.append(str(timeLimit)) #Time(s) - LS" "Sol.Quality - LS ", 
    CSVEntry.append(str(avgQuality)) #"Sol.Quality - LS 
    #==================

    LSTSol = float(avgQuality)
    BFError = float(CSVEntry[2]) / LSTSol
    CSVEntry[4] = str(BFError)


    ApproxRelError = float(CSVEntry[6]) / LSTSol
    CSVEntry[7] = str(ApproxRelError)

    CSVData.append(CSVEntry)



with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing data to the CSV file
    writer.writerows(CSVData)