from nba_api.stats.endpoints import shotchartdetail
import pandas as pd
import json
import requests
import datetime

class Query:
    def __init__(self, query=''):
        self.query = query
        self.data = self.get_data()
    
    def get_data(self):
        df = self.process_query()
        print('Query has been processed, and data has been returned')
        df = self.ShotTime(df)
        return df
    
    def process_query(self):
        query = self.validate_query(self.query)
        header, url_base = self.get_headers_url()
        parameters = {
        "AheadBehind": "",
        "CFID": "",
        "CFPARAMS": "",
        "ClutchTime": "",
        "Conference": "",
        "ContextFilter": "",
        "ContextMeasure": "FGA",
        "DateFrom": query[3],
        "DateTo": query[4],
        "Division": "",
        "EndPeriod": 10,
        "EndRange": 28800,
        "GROUP_ID": "",
        "GameEventID": "",
        "GameID": "",
        "GameSegment": "",
        "GroupID": "",
        "GroupMode": "",
        "GroupQuantity": 5,
        "LastNGames": query[2],
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OnOff": "",
        "OppPlayerID": "",
        "OpponentTeamID": 0,
        "Outcome": "",
        "PORound": 0,
        "Period": 0,
        "PlayerID": query[0],
        "PlayerID1": "",
        "PlayerID2": "",
        "PlayerID3": "",
        "PlayerID4": "",
        "PlayerID5": "",
        "PlayerPosition": "",
        "PointDiff": "",
        "Position": "",
        "RangeType": 0,
        "RookieYear": "",
        "Season": "2023-24",
        "SeasonSegment": "",
        "SeasonType": "Regular Season",
        "ShotClockRange": "",
        "StartPeriod": 1,
        "StartRange": 0,
        "StarterBench": "",
        "TeamID": query[1],
        "VsConference": "",
        "VsDivision": "",
        "VsPlayerID1": "",
        "VsPlayerID2": "",
        "VsPlayerID3": "",
        "VsPlayerID4": "",
        "VsPlayerID5": "",
        "VsTeamID": ""
        }
        response = requests.get(url_base, headers=header, params=parameters)
        response.raise_for_status()
        shots = response.json()['resultSets'][0]['rowSet']
        headers = response.json()['resultSets'][0]['headers']
        df = pd.DataFrame(shots, columns=headers)
        return df
    
    def get_headers_url(self):
        url_base = ' https://stats.nba.com/stats/shotchartdetail'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'stats.nba.com',
            'Origin': 'https://www.nba.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.nba.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'

        }
        return headers, url_base
    
    def validate_query(self, query, expected_length=5):
        query = query.split(',')
        self.validate_length(query, expected_length)
        query[0] = self.process_player(query[0])
        query[1] = self.process_team(query[1])
        query[2] = self.process_LastNGames(query[2])
        query[3], query[4] = self.process_Date(query[3]), self.process_Date(query[4])

        return query
    
    def validate_length(self, query, expected_length):
        if len(query) != expected_length:
            raise ValueError('Query is not the correct length')
        return True
    
    def process_player(self, player):
        if player == '0':
            return '0'
        with open('player_names.json') as f:
            player_names = json.load(f)
        if player not in player_names:
            raise ValueError('Player not found')
        playerID = player_names[player]
        return playerID
    
    def process_team(self, team):
        if team == '0':
            return '0'
        with open('team_names.json') as f:
            team_names = json.load(f)
        if team not in team_names:
            raise ValueError('Team not found')
        teamID = team_names[team]
        return teamID
    
    def process_LastNGames(self, LastNGames):
        if LastNGames == '0':
            return ''
        if not LastNGames.isdigit():
            raise ValueError('LastNGames is not an int')
        return LastNGames
    
    def process_Date(self, Date):
        if Date == '0':
            return ''
        if not Date.isdigit():
            raise ValueError('Date is not an int', Date)
        if len(Date) != 8:
            raise ValueError('Date is not in YYYYMMDD format', Date)
        yearFrom = int(Date[:4])
        monthFrom = int(Date[4:6])
        dayFrom = int(Date[6:])
        if monthFrom < 1 or monthFrom > 12:
            raise ValueError('Month is not valid,'+str(monthFrom))
        if dayFrom < 1 or dayFrom > 31:
            raise ValueError('Day is not valid,'+str(dayFrom))
        if yearFrom < 1996 or yearFrom > 2024:
            raise ValueError('Year is not valid,'+str(yearFrom))
        return Date
    
    def ShotTime(self, df):
        Cols = df.columns.values.tolist()
        Quarter = df[Cols[7]].tolist()
        StrMins = df[Cols[8]].tolist()
        StrSecs = df[Cols[9]].tolist()
        SecTime = []
        GameTime = []
        SecsinQ = 720
        for i in range(len(StrMins)):
            try:
                Org = str(StrMins[i])+":"+str(StrSecs[i])
                Add = "00:"
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

