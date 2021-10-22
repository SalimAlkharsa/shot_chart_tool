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
