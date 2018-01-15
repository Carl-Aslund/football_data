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

def classifyGame(selfScore, otherScore):
    """Calculate the value of a result from 0 (utter loss) to 1 (complete win)"""
    if otherScore == 0:
        if selfScore == 0:
            return 0.5 # Goalless draw
        else:
            return 1. # Win + Clean Sheet
    else:
        return selfScore/(selfScore+otherScore)

def matrixTable(season, gamesPlayed):
    """Uses the Mattingly method to rank teams in a partial season."""
    matchDict, teamDict = readMatchData(season)
    teamNames = list(sorted(teamDict.keys()))
    indexDict = {}
    for i in range(len(teamNames)):
        indexDict[teamNames[i]] = i
    A = np.array([[0.]*len(teamNames)]*len(teamNames))
    # A[1][0] = 5       Goes by A[row][col]
    unvisitedA = np.array([[True]*len(teamNames)]*len(teamNames))
    # When assessing a game, let p be the value of the win in the range (0.5, 1.0) based on the dominance of the win.
    # For each game, let i be the index of the winning team, and let j be the index of the losing team. Let aji = p and let aij = 1-p.
    for teamName in teamNames:
        team = teamDict[teamName]
        i = indexDict[teamName]
        fixtures = team.fixtureList
        for index in range(gamesPlayed):
            fixture = fixtures[index]
            matchup = fixture.getMatchup(teamName)
            matchData = matchDict[matchup]
            if fixture.atHome:
                p = classifyGame(matchData['homeGoals'],matchData['awayGoals'])
            else:
                p = classifyGame(matchData['awayGoals'],matchData['homeGoals'])
            j = indexDict[fixture.opponent]
            if unvisitedA[j][i]:
                A[j][i] = p
                unvisitedA[j][i] = False
            else:
                A[j][i] = (A[j][i] + p)/2
    # For each aii, let aii = (numGames) - sumj≠i(aij)
    for i in range(len(teamNames)):
        A[i][i] = gamesPlayed - sum(A[i])
    # A /= gamesPlayed
    # Rank teams by steady state vector (eigenvector associated with an eigenvalue of 1)
    w,v = la.eig(A) # Eigenvectors do not seem accurate
    print(w)


matrixTable('1617', 38)
