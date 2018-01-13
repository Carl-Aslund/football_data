'''This file will read in match data from csv files (obtained from football-data.co.uk) and proceed to generate standings for the teams, either on a match day or on a particular date, through the season.
'''

from models import Fixture, Position, Team
from datetime import date
import csv
# Imports for using matrices
from numpy import linalg as la
import numpy as np

def convertDate(dateStr):
    """Takes a date string from the data file to create a datetime object."""
    # Example 18/08/12 => datetime.date(2012, 8, 18)
    day, month, year = [int(x) for x in dateStr.split('/')]
    return date(year+2000, month, day) # Only works for seasons after 2000

def readMatchData(season):
    """Converts a particular season's csv file into more usable python formats."""
    matchDict = {}
    teamDict = {} # A dictionary of Team objects indexed by name
    seasonFile = open('match_data/'+season+'.csv')
    seasonReader = csv.reader(seasonFile)
    seasonData = list(seasonReader)
    #print(seasonData[0][1]) #[Row][Col]
    for i in range(1,381):
        # Gets all the data from rows 1-380
        homeTeam = seasonData[i][2]
        awayTeam = seasonData[i][3]
        matchup = (homeTeam, awayTeam)
        if homeTeam not in teamDict:
            teamDict[homeTeam] = Team(homeTeam)
        if awayTeam not in teamDict:
            teamDict[awayTeam] = Team(awayTeam)
        teamDict[homeTeam].addFixture(matchup)
        teamDict[awayTeam].addFixture(matchup)
        matchDict[matchup] = {'date':convertDate(seasonData[i][1]), 'homeGoals':int(seasonData[i][4]), 'awayGoals':int(seasonData[i][5]), 'resultChar':seasonData[i][6]}
    return matchDict, teamDict


readMatchData('1617')
