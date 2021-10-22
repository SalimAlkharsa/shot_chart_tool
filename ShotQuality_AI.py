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

'''
This program is made to quantify shot quality via a machine learning model,
still in development.
'''


def ApplyModel(df):
    #The Machine Learning Section
    #Labelling the Train DF
    Cols = df.columns.values.tolist()
    Trainx = df
    Trainy = df[Cols[5]].tolist()
    ToDrop = [Cols[5]]
    Trainx = df.drop(ToDrop, axis = 1)
    #Building the model
    model = RandomForestClassifier()
    model.fit(Trainx, Trainy)
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    n_scores = cross_val_score(model, Trainx, Trainy, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
    # report performance
    print('Accuracy: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
    return model

def TestingFunc(model):
    #Testing the Model
    df = ScrapeData(TeamID, PlayerID, LastNGames = 0, Season = '2019-20')
    Cols = df.columns.values.tolist()
    
    #Apply functions 
    df = ShotTime(df, Cols) 
    
    #Removing Unwanted
    Cols = df.columns.values.tolist()
    '''
    ToDrop = [Cols[0], Cols[1],Cols[2],Cols[3],Cols[4],Cols[5],Cols[6],
              Cols[7], Cols[10],Cols[11],Cols[12],Cols[13],Cols[14], Cols[15],
              Cols[19],Cols[21],Cols[22], Cols[23]] #A list of columns I dont want
    df = df.drop(ToDrop, axis = 1)
    '''
    
    #The Machine Learning Section
    #Labelling the Train DF
    
    Cols = df.columns.values.tolist()
    Testx = df
    Testy = df[Cols[5]].tolist()
    
    ToDrop = [Cols[5]]
    Testx = df.drop(ToDrop, axis = 1)
    
    yhat = model.predict(Testx)
    
    Error = []
    
    for i in range(len(Testy)):
        error = yhat[i]-Testy[i]
        sq = error*error
        root = sq**(0.5)
        Error.append(root)
        
    print("Mean: ",s.mean(Error),"SD: ",s.pstdev(Error))