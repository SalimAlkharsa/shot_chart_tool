#Imports
import pandas as pd

'''
This program has the purpose of finding team shooting, when one player is not on the court
'''



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
        
        
    