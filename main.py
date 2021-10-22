#Imports
import pandas as pd
import datetime
import numpy as np
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import teams
from nba_api.stats.static import players
import requests
import json
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
import statistics as s
import math as m

#Import of Other Files
from Scrape_CleanShotData import CleanData as SCD

def GetData():
    #Loading basic info by getting user input
    print("This is the shot scraping and analysis program, follow the instructions below to go through the program...")
    DataType = input("  Input 1 if you want a team's data; 2 if you want a player's data (If you screw this step up, the program will crash so enter a 1 or a 2...): ")
    #Team info
    nba_teams = teams.get_teams()
    nba_players = players.get_players()
    TeamID = 0
    PlayerID = 0
    if(DataType == 1):
        while(True):
            try:
                TeamAbb = input("       Input the team abbreviation you need data for, if you want all team's data enter 0! ")
                if(TeamAbb=='0'):
                    TeamID = 0
                else:
                    Team = [team for team in nba_teams if team['abbreviation'] == TeamAbb][0]
                False
            except:
                print("Try again, input could not be read...")
    if(DataType == 2):
        while(True):
            try:
                PlayerIn = input("       Input the player full name you need data for, if you want all player's data enter 0! ")
                if(PlayerIn=='0'):
                    PlayerID = 0
                else:
                    Player = [player for player in nba_players if player['full_name'] == PlayerIn][0]
                False
            except:
                print("Try again, input could not be read...")
    print("A few more things...")
    Season = input("Enter the season data you want (Format ex 2021-22): ")
    LastNGames = input("Enter the last LastNGames you want data for (if all games put 0): ")
    return TeamID, PlayerID, LastNGames, Season

if __name__ == '__main__':
    
    
    TeamID = GetData()[0]
    PlayerID = GetData()[1]
    LastNGames = GetData()[2]
    Season = GetData()[3]
    
    df = SCD.CleanData(TeamID, PlayerID, LastNGames, Season)
    df.to_csv("PlayerData.csv")
    #Cols = df.columns.values.tolist()
