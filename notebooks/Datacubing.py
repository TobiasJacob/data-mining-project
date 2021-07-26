#%%
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import datetime
import seaborn as sns
from sklearn.cluster import KMeans
from pathlib import Path

from pathlib import Path
Path("../reports/2/tables").mkdir(parents=True, exist_ok=True)

sns.set_style("whitegrid")


#%%
con = sqlite3.connect('reducedDataset.sqlite') # Write data

#%% Fix dtypes dfGames
dfGames = pd.read_sql("SELECT * FROM Game", con, index_col="index")
dfGames["SEASON"] = pd.to_numeric(dfGames["SEASON"])
dfGames["GAME_DATE"] = pd.to_datetime(dfGames["GAME_DATE"])
dfGames["FG3M_HOME"] = pd.to_numeric(dfGames["FG3M_HOME"])
dfGames["FG3A_HOME"] = pd.to_numeric(dfGames["FG3A_HOME"])
dfGames["FGA_HOME"] = pd.to_numeric(dfGames["FGA_HOME"])
dfGames["FGA_AWAY"] = pd.to_numeric(dfGames["FGA_AWAY"])
dfGames["FG3M_AWAY"] = pd.to_numeric(dfGames["FG3M_AWAY"])
dfGames["FG3A_AWAY"] = pd.to_numeric(dfGames["FG3A_AWAY"])
dfGames.dtypes

#%% Fix dtypes dfPlayers
dfPlayers = pd.read_sql("SELECT * FROM Player_Attributes", con, index_col="ID").drop("index", axis=1)
dfPlayers["FROM_YEAR"] = pd.to_numeric(dfPlayers["FROM_YEAR"])
dfPlayers["BIRTHDATE"] = pd.to_datetime(dfPlayers["BIRTHDATE"])
dfPlayers["FROM_YEAR"] = pd.to_numeric(dfPlayers["FROM_YEAR"])
dfPlayers["TO_YEAR"] = pd.to_numeric(dfPlayers["TO_YEAR"])
dfPlayers.dtypes

#%% Fix dtypes dfPlayerSalary
dfTeams = pd.read_sql("SELECT * FROM Team_Attributes", con, index_col="ID").drop("index", axis=1)
dfTeams.dtypes

#%% Fix dtypes dfPlayerSalary
dfPlayerSalary = pd.read_sql("SELECT * FROM Player_Salary", con, index_col="namePlayer").drop("index", axis=1)
dfPlayerSalary.dtypes

# %% Outlier fixing
# Fix active years for 
dfPlayers.loc["76114", "FROM_YEAR"] = 1951
dfPlayers.loc["76114", "TO_YEAR"] = 1956

# %%
dfPlayers

# %%
cubeGames = dfGames.join(
    dfTeams, on="TEAM_ID_HOME", how="left", rsuffix="HOME_TEAM"
).join(
    dfTeams, on="TEAM_ID_AWAY", how="left", rsuffix="AWAY_TEAM"
).drop(["TEAM_ID_HOME", "TEAM_ID_AWAY"], axis=1)
cubeGames.to_csv("cubeGames.csv")
cubeGames.head(10).to_latex("../reports/2/tables/cubeGames.tex")
cubeGames.tail()

# %%
dfPlayers["FULL_NAME"] = dfPlayers["FIRST_NAME"] + " " + dfPlayers["LAST_NAME"]
cubePlayers = dfPlayers.join(
    dfPlayerSalary.groupby("namePlayer").mean(), on="FULL_NAME", how="left"
).join(
    dfTeams,
    how="left"
).drop(['TEAM_ID'], axis=1)
cubePlayers["AGE"] = (datetime.datetime.now() - dfPlayers["BIRTHDATE"]) / datetime.timedelta(days=365)
cubePlayers["FROM_YEAR_AGE"] = dfPlayers["FROM_YEAR"] - dfPlayers["BIRTHDATE"].dt.year
cubePlayers["TO_YEAR_AGE"] = dfPlayers["TO_YEAR"] - dfPlayers["BIRTHDATE"].dt.year
cubePlayers["ACTIVE_YEARS"] = dfPlayers["TO_YEAR"] - dfPlayers["FROM_YEAR"]
cubePlayers.loc[cubePlayers["POSITION"] == "Center-Forward", "POSITION"] = "Forward-Center"
cubePlayers.loc[cubePlayers["POSITION"] == "Guard-Forward", "POSITION"] = "Forward-Guard"
cubePlayers.tail()

cubeGames.head(10).to_latex("../reports/2/tables/cubePlayers.tex")
cubePlayers.to_csv("cubePlayers.csv")
# %%
biometricCube = cubePlayers[["FULL_NAME", "TEAM_NAME", "HEIGHT", "WEIGHT", "PTS", "POSITION", "ACTIVE_YEARS"]].copy()
biometricCube.to_csv("biometricCubeRaw.csv")
biometricCube
#%%
def discretize(cube, key: str, labels: List[str]):
    # pass # Debugging
    # cube=biometricCube
    # key="HEIGHT"
    # labels=["Short", "Middle", "Tall"]
    labels = np.array(labels)
    col = cube[[key]]
    ind = ~col[key].isna()
    kmeans = KMeans(init="random", n_clusters=len(labels)).fit(col[ind])
    clusterOrder = np.argsort(np.argsort(kmeans.cluster_centers_[:, 0]))
    cube[key] = "N/A"
    cube[key][ind] = labels[clusterOrder[kmeans.labels_]]
    clusterBorders = np.sort(kmeans.cluster_centers_[:, 0])
    clusterBorders = (clusterBorders[:-1] + clusterBorders[1:]) / 2
    clusterBorders = np.stack((col.min()[0], *clusterBorders, col.max()[0]))
    for (lab, lowVal, highVal) in zip(labels, clusterBorders[:-1], clusterBorders[1:]):
        print(f"{lab}: {(cube[key] == lab).sum()} values, [{lowVal:2.2f}, {highVal:2.2f}]")

    sns.displot(col, kind="kde")
    plt.plot(kmeans.cluster_centers_, np.zeros_like(kmeans.cluster_centers_), "o")
    Path("../reports/2/figures/disc").mkdir(parents=True, exist_ok=True)
    plt.savefig(f"../reports/2/figures/disc/{key}.eps")

# %%
discretize(biometricCube, "HEIGHT", ["Short", "Middle", "Tall"])
biometricCube

# %%
discretize(biometricCube, "WEIGHT", ["Light", "Middle", "Heavy"])
biometricCube

# %%
discretize(biometricCube, "PTS", ["LessScores", "MiddleScores", "MoreScores", "ManyScores"])
biometricCube

# %%
discretize(biometricCube, "ACTIVE_YEARS", ["Short", "Middle", "Long"])
biometricCube

#%%
biometricCube.to_csv("biometricCube.csv")
biometricCube.tail(20).to_latex("../reports/2/tables/biometricCubeTable.tex")

# %%

# %%
