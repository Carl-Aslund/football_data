'''This file contains usable classes for other files in the directory.'''

class Fixture():

    def __init__(self, name, teams):
        if name == teams[0]:
            self.opponent = teams[1]
            self.atHome = True
        elif name == teams[1]:
            self.opponent = teams[0]
            self.atHome = False
        else:
            print("ERROR: Team does not match teams in match data.")

    def __str__(self):
        token = "A" # Away
        if self.atHome:
            token = "H" # Home
        return self.opponent + " (" + token + ")"

    def getMatchup(self, name):
        """Converts a fixture into a 2-tuple of opponents."""
        if self.atHome:
            return (name, self.opponent)
        else:
            return (self.opponent, name)

class Team():

    def __init__(self, teamName):
        self.name = teamName
        self.fixtureList = []

    def addFixture(self, matchup):
        self.fixtureList.append(Fixture(self.name, matchup))

    def __str__(self):
        return self.name

class Position():

    def __init__(self, numGames, team, matchData):
        self.points = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.gamesPlayed = 0
        self.teamName = team.name
        for fixture in team.fixtureList:
            if self.gamesPlayed == numGames:
                break
            match = matchData[fixture.getMatchup(self.teamName)]
            if match['resultChar'] == 'D':
                self.points += 1
            # Add results of match to appropriate categories
            self.gamesPlayed += 1
            if fixture.atHome:
                if match['resultChar'] == 'H':
                    self.points += 3
                self.goalsFor += match['homeGoals']
                self.goalsAgainst += match['awayGoals']
            else:
                if match['resultChar'] == 'A':
                    self.points += 3
                self.goalsFor += match['awayGoals']
                self.goalsAgainst += match['homeGoals']

    def goalDiff(self):
        return self.goalsFor - self.goalsAgainst

    def __gt__(self, other):
        """Determines if self>other"""
        if self.points != other.points:
            return self.points > other.points
        elif self.goalDiff() != other.goalDiff():
            return self.goalDiff() > other.goalDiff()
        elif self.goalsFor != other.goalsFor:
            return self.goalsFor > other.goalsFor
        else:
            return self.teamName < other.teamName

    def __str__(self):
        return "GP:\t" + str(self.gamesPlayed) + "\nPoints:\t" + str(self.points) + "\nGF:\t" + str(self.goalsFor) + "\nGA:\t" + str(self.goalsAgainst)
