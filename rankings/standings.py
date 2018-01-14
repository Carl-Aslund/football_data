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
    for i in range(1,381):
        # Gets all the data from rows 1-380
        # Only works for a 380-game season
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

def getTeamPosition(season, teamName):
    """Creates a Position object for a team in a 38-game season."""
    matchDict, teamDict = readMatchData(season)
    teamPosition = Position(38, teamDict[teamName], matchDict)
    print(teamPosition)

def getTable(season, gamesPlayed):
    """Creates a table of team positions after all teams have played some number of games."""
    matchDict, teamDict = readMatchData(season)
    positionDict = {}
    for team in teamDict.values():
        positionDict[team] = Position(gamesPlayed, team, matchDict)
    for team in sorted(positionDict, key=positionDict.get, reverse=True):
        print(team)

print("0 games in:")
getTable('1617', 0)
print("\n19 games in:")
getTable('1617', 19)
print("\n38 games in:")
getTable('1617', 38)
