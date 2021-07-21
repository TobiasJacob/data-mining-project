#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import datetime
import seaborn as sns
sns.set_style("whitegrid")
# %%
cubeGames = pd.read_csv("cubeGames.csv")
cubePlayers = pd.read_csv("cubePlayers.csv")
biometricCube = pd.read_csv("biometricCube.csv")
cubeGames["GAME_DATE"] = pd.to_datetime(cubeGames["GAME_DATE"])
cubePlayers["BIRTHDATE"] = pd.to_datetime(cubePlayers["BIRTHDATE"])

# %%
sns.lmplot('ACTIVE_YEARS', 'PTS', data=cubePlayers, hue='POSITION', fit_reg=False)

#%%
sns.lmplot('ACTIVE_YEARS', 'PTS', cubePlayers.groupby("POSITION").mean().reset_index(), hue='POSITION')

# %%
sns.lmplot('ACTIVE_YEARS', 'PTS', data=cubePlayers, fit_reg=True)
plt.title("Active years and player points")

# %%
sns.lmplot('HEIGHT', 'PTS', data=cubePlayers, fit_reg=False)
plt.title("Player height and points")

# %%
sns.distplot(cubePlayers[["FROM_YEAR_AGE"]], hist=False, rug=True)
sns.distplot(cubePlayers[["TO_YEAR_AGE"]], hist=False, rug=True)
plt.xlim(15,40)
plt.xticks(np.arange(15, 40, 1.0))
plt.legend(["Starting", "Leaving"])
plt.xlabel("Player Age")
pass
# %%
cubeGames.pivot_table(
    values="PTS_HOME",
    index="TEAM_NAME_HOME",
    columns=None,
    aggfunc=np.sum
)
# %%
cubeGames.pivot_table(
    values="PTS_HOME",
    index="SEASON",
    columns=None,
    aggfunc=np.count_nonzero
).plot()
plt.title("How the NBA grew")
plt.legend(["Games"])
# %%
