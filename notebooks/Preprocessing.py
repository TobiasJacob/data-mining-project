# %% Import frameworks
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# %% Connect to databases
con = sqlite3.connect('../archive/basketball.sqlite') # Read in data
conOut = sqlite3.connect('reducedDataset.sqlite') # Write data

# %% Convert GameDatabase
def reduceData(tableName: str, columnsToKeep: str):
    df = pd.read_sql(f'SELECT * FROM {tableName} LIMIT 10', con) # Make a small request with all columns
    print("---Reducing", tableName, "---\n")
    print("Columns before: ", ", ".join([f"{colName}" for (colName, val) in zip(df.columns, df.iloc[1])]), "\n")
    print("Columns after reduction: ", columnsToKeep, "\n")
    df = pd.read_sql(f'SELECT {columnsToKeep} FROM {tableName}', con) # Request only columnsToKeep
    print("Total number of rows: ", df.shape[0], "\n") # Print the number of rows
    print("Null values found: ", df.isnull().sum(), "\n") # Count null values found by attribute
    df = df.dropna() # Drop rows with missing values
    print("Total number of rows after dropna: ", df.shape[0], "\n")
    print("Null values found after dropna (testing): ", df.isnull().sum(), "\n")
    df.to_sql(tableName, conOut, if_exists = "replace")

# %% convert Game
columnsToKeep = "TEAM_ID_HOME, TEAM_NAME_HOME, TEAM_ID_AWAY, TEAM_NAME_AWAY, GAME_DATE, SEASON, HOME_TEAM_WINS, HOME_TEAM_LOSSES, PTS_HOME, PTS_AWAY, FGM_HOME, FGA_HOME, FG3M_HOME, FG3A_HOME, FTM_HOME, FTA_HOME, FGM_AWAY, FGA_AWAY, FG3M_AWAY, FG3A_AWAY, FTM_AWAY, FTA_AWAY"
reduceData("Game", columnsToKeep)

# %% convert Player_Attributes
columnsToKeep = "ID, FIRST_NAME, LAST_NAME, BIRTHDATE, HEIGHT, WEIGHT, PTS, TEAM_ID, TEAM_NAME, FROM_YEAR, TO_YEAR"
reduceData("Player_Attributes", columnsToKeep)

# %% convert Team_Attributes
columnsToKeep = "ID, YEARFOUNDED, CITY, NICKNAME"
reduceData("Team_Attributes", columnsToKeep)
