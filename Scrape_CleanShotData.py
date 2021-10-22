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
import math as m
'''
This file is used to scrape all the data related to shot charts from the NBA Website with the goal of
organizing it for use
'''

#Functions used in the program
def ScrapeData(TeamID, PlayerID, LastNGames, Season):
    '''
    This function is made to scrape data, defaulting PlayerID and TeamId to 0
    makes it load every player/team
    '''
    response = shotchartdetail.ShotChartDetail(
	team_id= TeamID, 
	player_id= PlayerID, #initialize variable here
	season_nullable= Season,
	season_type_all_star='Regular Season'
    )
    
    content = json.loads(response.get_json())
    
    url_base = 'https://stats.nba.com/stats/shotchartdetail'
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    parameters = {
    	'ContextMeasure': 'FGA',
    	'LastNGames': LastNGames, 
    	'LeagueID': '00',
    	'Month': 0,
    	'OpponentTeamID': 0, #Add more functions to optimize this
    	'Period': 0,
    	'PlayerID': PlayerID, #initialize variable here
    	'SeasonType': 'Regular Season', #One of [Regular Season Pre SeasonPlayoffs]
    	'TeamID': TeamID,  #initialize variable here
    	'VsDivision': '',
    	'VsConference': '',
    	'SeasonSegment': '', #((Post All-Star)|(Pre All-Star))
    	'Season': Season,
    	'RookieYear': '',
    	'PlayerPosition': '',
    	'Outcome': '',
    	'Location': '',
    	'GameSegment': '', #((First Half)|(Overtime)|(Second Half))
    	'GameId': '',
    	'DateTo': '',
    	'DateFrom': '',
        'ClutchTime': '' #((Last 5 Minutes)|(Last 4 Minutes)|(Last 3 Minutes)|(Last 2 Minutes)|(Last 1 Minute)|(Last 30 Seconds)|(Last 10 Seconds))
    } #Here it is a bunch of filters
    
    response = requests.get(url_base, params=parameters, headers=headers)
    content = json.loads(response.content)
    
    # transform contents into dataframe
    results = content['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    df = pd.DataFrame(rows)
    df.columns = headers
    
    return df

def ShotTime(df):
    '''
    This function here will find the time the shot was taken by turning the string Time
    column to seconds and then multiplying that by quarter and then taking the new seconds
    value and making minutes and putting it back in the df. Works for OT as well
    '''
    Cols = df.columns.values.tolist()
    Quarter = df[Cols[7]].tolist()
    StrMins = df[Cols[8]].tolist()
    StrSecs = df[Cols[9]].tolist()
    SecTime = []
    GameTime = []
    SecsinQ = 720
    
    #Some editing to turn the time from string to seconds
    for i in range(len(StrMins)):
        try:
            Org = str(StrMins[i])+":"+str(StrSecs[i])
            Add = "00:"
            '''
            This next 2 lines was partially modified from Stack Overflow
            '''
            hhmmss = Add+Org
            [hours, minutes, seconds] = [int(x) for x in hhmmss.split(':')]
            x = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            SecTime.append(x.seconds)
        except IndexError:
            continue
            print("Hi")
            
    for i in range(0, len(Quarter)):
        try:
            if SecTime == 0: 
                continue
            else:
                n = ((Quarter[i]-1) *SecsinQ) +(720-SecTime[i])
                Minute = n//60
                GameTime.append(Minute)
        except IndexError:
            continue
            print("Hi")
            
    df["Time In the Game"] = pd.Series(GameTime)
    
    return df

def CleanData(TeamID, PlayerID, LastNGames, Season):
    #Loading the data and doing it as wanted
    df = ScrapeData(TeamID, PlayerID, LastNGames, Season) #Here you can control what data is scraped
    Cols = df.columns.values.tolist()
    
    #Apply functions 
    df = ShotTime(df) 
    df = ShotAngleAdv(df)
    df = IntegratingPlayerInfo(df)
    #Removing Unwanted
    '''
    Cols = df.columns.values.tolist()
    ToDrop = [Cols[0], Cols[1],Cols[2],Cols[3],Cols[4],Cols[5],Cols[6],
              Cols[7], Cols[10],Cols[11],Cols[12],Cols[13],Cols[14], Cols[15],
              Cols[19],Cols[21],Cols[22], Cols[23]] #A list of columns I dont want
    df = df.drop(ToDrop, axis = 1)
    '''
    df = df.dropna(axis=0)
    
    return df

def ShotAngleAdv(df):
    '''
    This function will first calculate the magnitude of the shot angle and then it will
    use that information to calculate the shot area as a sin or cos value depending on
    if the angle is more than or less than 45. The objective is to essentially see how
    where on the court a shot is taken regardless of left or right side of the court
    '''
    Cols = df.columns.values.tolist()
    X = df[Cols[17]].tolist()
    Y = df[Cols[18]].tolist()
    #Finding the shot angle regardless of sign
    angles = []
    for i in range(len(X)):
        y = Y[i]
        x = X[i]
        try:
            n = m.atan(y/x) #use atan2 if signs should be considered
        except ZeroDivisionError:
            n = 0
        degree = m.degrees(n)
        mag = abs(degree)
        angles.append(mag)
    #Now we apply the tightness adjustment
    Ang = []
    for i in angles:
        x = m.radians(i)
        if x <= m.radians(45):
            Ang.append(m.cos(x))
        elif x > m.radians(45):
            Ang.append(m.sin(x))
    #Apply changes
    df["ShotTightness"] = pd.Series(Ang)
    
    return df
    
def PlayerInfoDF():
    '''
    Here I want to add info related to the player like his height, weight, and
    other things I can quickly pick off
    '''
    url = 'https://stats.nba.com/stats/playerindex'
    #Header Tab, under "Query String Parameter" subsection
    params =(
    ("College",""),
    ("Country",""),
    ("DraftPick",""),
    ("DraftRound",""),
    ("DraftYear",""),
    ("Height",""),
    ("Historical", 0),
    ("LeagueID", "00"),
    ("Season", "2021-22"),
    ("SeasonType", "Regular Season"),
    ("TeamID", 0),
    ("Weight",""))
    # Header tab, under “Request Headers” subsection
    header = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.nba.com",
    "referer": "https://www.nba.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true"}
    #Using Request library to get the data
    response = requests.get(url, headers=header, params=params)
    response_json = response.json()
    df = pd.DataFrame(response_json['resultSets'][0]['rowSet'])
    df.columns = response_json['resultSets'][0]['headers']
    return df
    
def IntegratingPlayerInfo(df):
    '''
    This function will add player info as a feature to the primary df
    '''
    ColsDF = df.columns.values.tolist()
    ID_List = df[ColsDF[3]].tolist()
    totalR = len(ID_List)
    
    Height = [None]*totalR
    Weight = [None]*totalR
    Experience = [None]*totalR
    
    UniqueID = IdenticalID(df)
    IdenticalRows = []
    
    X = PlayerInfoDF() #Here we get the player info
    ColX = X.columns.values.tolist()
    
    #First deal with the heights, make them a usable column within X
    HeightStr = X[ColX[12]].tolist()
    Heights = []
    for n in range(len(HeightStr)):
        dummy = HeightStr[n].split("-")
        ft = dummy[0]
        inch = dummy[1]
        Inches = float(ft)*12+float(inch)
        Heights.append(Inches)
    X[ColX[12]] = pd.Series(Heights)    
    #Now we want a usable experience column
    Begin = X[ColX[20]].tolist()
    End = X[ColX[21]].tolist()
    
    Experience = []
    for i in range(len(Begin)):
        initial = float(Begin[i])
        final = float(End[i])
        Experience.append(final-initial)
    X["Experience"] = pd.Series(Experience)
    
    ####
    ColsDF = df.columns.values.tolist()
    ColX = X.columns.values.tolist()
    
    XID = X[ColX[0]].tolist()
    DFID = df[ColsDF[3]].tolist()
    
    Height = [None]*totalR
    Weight = [None]*totalR
    Experience = [None]*totalR
    
    XHeights = X[ColX[12]].tolist()
    XWeights = X[ColX[13]].tolist()
    XExperience = X[ColX[26]].tolist()
    
    for i in range(len(DFID)):
        for j in range(len(XID)):
            if DFID[i] == XID[j]:
                try:
                    #That means we have a match
                    Height[i] = XHeights[j]
                    Weight[i] = XWeights[j]
                    Experience[i] = XExperience[j]
                except IndexError:
                    break
                
    df["Height"] = pd.Series(Height)
    df["Weight"] = pd.Series(Weight)
    df["Experience"] = pd.Series(Experience)     
        
    return df
 
def FTInfo(PlayerID):
    '''
    Here I will grab each player's free throw shooting percentage as a baseline way of
    guaging if they are a good shooter or not.
    '''
    url = ' https://stats.nba.com/stats/leaguedashplayerstats'
    #Header Tab, under "Query String Parameter" subsection
    params =(
    ("College",""),
    ("Conference",""),
    ("Country",""),
    ("DateFrom",""),
    ("DateTo",""),
    ("Division",""),
    ("DraftPick",""),
    ("DraftYear",""),
    ("GameScope",""),
    ("GameSegment",""),
    ("Height",""),
    ("LastNGames", 0),
    ("LeagueID", "00"),
    ("Location",""),
    ("MeasureType", "Base"),
    ("Month", 0),
    ("OpponentTeamID", 0),
    ("Outcome",""),
    ("PORound", 0),
    ("PaceAdjust", "N"),
    ("PerMode", "PerGame"),
    ("Period", 0),
    ("PlayerExperience",""),
    ("PlayerPosition",""),
    ("PlusMinus", "N"),
    ("Rank", "N"),
    ("Season", "2021-22"),
    ("SeasonSegment",""),
    ("SeasonType", "Regular Season"),
    ("ShotClockRange",""),
    ("StarterBench",""),
    ("TeamID", 0),
    ("TwoWay", 0),
    ("VsConference",""),
    ("VsDivision",""),
    ("Weight",""))
    # Header tab, under “Request Headers” subsection
    header = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.nba.com",
    "referer": "https://www.nba.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true"}
    #Using Request library to get the data
    response = requests.get(url, headers=header, params=params)
    response_json = response.json()
    df = pd.DataFrame(response_json['resultSets'][0]['rowSet'])
    df.columns = response_json['resultSets'][0]['headers']
    
    return df
    
def IdenticalID(df): #Func not in use
    '''
    This is intended to quicken the collection of data by reducing the requests and
    finding rows in the df that have the same ID and collecting what those rows are
    '''
    Cols = df.columns.values.tolist()
    ID_List = df[Cols[3]].tolist()
    UniqueID = []
    for i in ID_List:
        if i not in UniqueID:
            UniqueID.append(i)
        else: 
            continue
    return UniqueID