#Imports
import pandas as pd

'''
This program has the purpose of finding team shooting, when one player is not on the court
'''

def RowsWithOutPlayer(df, PlayerChecked):
    #This is a rough approximation, where the min/FGA is used to see if the player is on or not
    #So for example if someone takes 15FGA in 32mins then 2.13 is min/FGA
    #So if there are 100 mins recorded then if the player does not show up in the last
    #min/FGA+min/FGA*0.5 then he is assumed to be off the court (or at least not impacting the game)
    FGAG = float(input("Enter FGA/g for your player: "))
    mins = float(input("Enter mins/g for your player: "))
    minFGA = mins/FGAG
    min = df["Time In the Game"]
    min = min.to_list()
    Shooter = df["PLAYER_NAME"]
    Shooter = Shooter.to_list()
    LastShot = 0
    RowsNotPlaying = []
    for row in range(1, len(min)):
        #For each row, get the min and see if the player took a shot...
        if(Shooter[row] != PlayerChecked and min[row]!=min[row-1]):
            LastShot += 1
        elif(Shooter[row] == PlayerChecked):
            LastShot = 0
        else:
            LastShot = LastShot
        #Now we know how long it has been since the last shot
        if(LastShot >= minFGA):
            RowsNotPlaying.append(row)
    return RowsNotPlaying

def DFwoPlayer(df, DelRows):
    df.drop(DelRows, inplace=True)
    return df



#main
#LoadDF
File = input("Enter the team filename with the csv included: ")
PlayerChecked = input("Enter the name of the player you are evaluating: ")
df = pd.read_csv(File)
DelRows = RowsWithOutPlayer(df, PlayerChecked)
df = DFwoPlayer(df, DelRows)     
        
        
    