#Imports
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import shotchartlineupdetail
import requests
import json
'''
This program has the purpose of finding team shooting, when one player is not on the court
'''

'''
Links I want...
https://www.nba.com/stats/events/?flag=3&CFID=&CFPARAMS=&PlayerID=0&TeamID=1610612752&GameID=&ContextMeasure=FGA&Season=2020-21&SeasonType=Regular%20Season&LeagueID=00&PerMode=Totals&GroupQuantity=5&PlusMinus=N&PaceAdjust=N&Rank=N&Outcome=&Location=&Month=0&SeasonSegment=&OpponentTeamID=0&VsConference=&VsDivision=&GameSegment=&Period=0&LastNGames=0&DateFrom=&DateTo=&ShotClockRange=&Conference=&Division=&PORound=0&MeasureType=Base&section=lineups&islineup=1&GROUP_ID=-201565-201959-202692-1630167-1630193-&GroupID=-201565-201959-202692-1630167-1630193-&sct=hex
https://www.nba.com/stats/events/?flag=3&CFID=&CFPARAMS=&PlayerID=0&TeamID=1610612752&GameID=&ContextMeasure=FGA&Season=2020-21&SeasonType=Regular%20Season&LeagueID=00&PerMode=Totals&GroupQuantity=5&PlusMinus=N&PaceAdjust=N&Rank=N&Outcome=&Location=&Month=0&SeasonSegment=&OpponentTeamID=0&VsConference=&VsDivision=&GameSegment=&Period=0&LastNGames=0&DateFrom=&DateTo=&ShotClockRange=&Conference=&Division=&PORound=0&MeasureType=Base&section=lineups&islineup=1&GROUP_ID=-203085-203457-1628995-1630167-1630193-&GroupID=-203085-203457-1628995-1630167-1630193-
ex group id: 
'''
#https://stats.nba.com/stats/shotchartlineupdetail?ContextFilter=&ContextMeasure=PTS&DateFrom=&DateTo=&GROUP_ID=-201565-201959-202692-1630167-1630193-&GameID=&GameSegment=&LastNGames=&LeagueID=00&Location=&Month=&OpponentTeamID=&Outcome=&Period=0&Season=2020-21&SeasonSegment=&SeasonType=Regular+Season&TeamID=1610612752&VsConference=&VsDivision=
  
def GetSpecificData():
    nba_teams = teams.get_teams()
    nba_players = players.get_players()
    n = True
    while(n==True):
        try:
            TeamAbb = input("       Input the team abbreviation you need data for, if you want all team's data enter 0! ")
            if(TeamAbb=='0'):
                TeamID = 0
            else:
                Team = [team for team in nba_teams if team['abbreviation'] == TeamAbb][0]
                TeamID = Team['id']
            n=False
        except:
            print("Try again, input could not be read...")
    n = True
    while(n==True):
        try:
            PlayerIn = input("       Input the player full name you need data for, if you want all player's data enter 0! ")
            if(PlayerIn=='0'):
                PlayerID = 0
            else:
                Player = [player for player in nba_players if player['full_name'] == PlayerIn][0]
                PlayerID = Player['id'] 
            n=False
        except:
            print("Try again, input could not be read...")
    print("A few more things...")
    Season = input("Enter the season data you want (Format ex 2021-22): ")
    LastNGames = input("Enter the last LastNGames you want data for (if all games put 0): ")
    SaveAS = input("Lastly what do you want to save the file as (Enter FileName only, csv is autoadded): ")
    return TeamID, PlayerID, LastNGames, Season, SaveAS

def ScrapeLineUpData(TeamID, PlayerID, GroupID, Season, LastNGames):
    '''
    This function is made to scrape data, defaulting PlayerID and TeamId to 0
    makes it load every player/team
    '''
    response = shotchartlineupdetail.ShotChartLineupDetail(
	team_id= TeamID, 
	player_id= PlayerID, #initialize variable here
	season_nullable= Season,
	season_type_all_star='Regular Season'
    )
    
    content = json.loads(response.get_json())
    
    url_base = 'https://stats.nba.com/stats/shotchartlineupdetail'
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
    'GROUP_ID': GroupID,
    'LeagueID': '00',
    'Period': '00',
    'Season': Season,
    'SeasonType': '',
    'ContextFilter': '',
    'DateFrom': '',
    'DateTo': '',
    'GameID': '',
    'GameSegment': '',
    'LastNGames': LastNGames,
    'Location': '',
    'Month': '',
    'OpponentTeamID': '',
    'Outcome': '',
    'SeasonSegment': '',
    'TeamID': '',
    'VsConference': '',
    'VsDivision': ''
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


#main

GroupID = '-201565-201959-202692-1630167-1630193'
#LoadDF
Data = GetSpecificData()
TeamID = Data[0]
PlayerID = Data[1]
LastNGames = Data[2]
Season = Data[3]
SaveAs = Data[4]
df = ScrapeLineUpData(TeamID, PlayerID, GroupID, Season, LastNGames)
