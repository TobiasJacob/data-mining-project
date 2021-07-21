#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import datetime
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
Path("../reports/2/figures").mkdir(parents=True, exist_ok=True)
# %%
cubeGames = pd.read_csv("cubeGames.csv")
cubePlayers = pd.read_csv("cubePlayers.csv")
biometricCube = pd.read_csv("biometricCube.csv")
cubeGames["GAME_DATE"] = pd.to_datetime(cubeGames["GAME_DATE"])
cubePlayers["BIRTHDATE"] = pd.to_datetime(cubePlayers["BIRTHDATE"])

# %%
sns.lmplot('ACTIVE_YEARS', 'PTS', data=cubePlayers, hue='POSITION', fit_reg=False)
plt.savefig(f"../reports/2/figures/ACTIVE_YEARS_over_PTS.eps")

#%%
sns.lmplot('ACTIVE_YEARS', 'PTS', cubePlayers.groupby("POSITION").mean().reset_index(), hue='POSITION')
plt.savefig(f"../reports/2/figures/ACTIVE_YEARS_over_PTS_Grouped.eps")

# %%
sns.lmplot('ACTIVE_YEARS', 'PTS', data=cubePlayers, fit_reg=True)
# plt.title("Active years and player points")
plt.savefig(f"../reports/2/figures/ACTIVE_YEARS_over_PTS2.eps")

# %%
sns.lmplot('HEIGHT', 'PTS', data=cubePlayers, fit_reg=False)
# plt.title("Player height and points")
plt.savefig(f"../reports/2/figures/HEIGHT_over_PTS2.eps")

# %%
sns.distplot(cubePlayers[["FROM_YEAR_AGE"]], hist=False, rug=True)
sns.distplot(cubePlayers[["TO_YEAR_AGE"]], hist=False, rug=True)
plt.xlim(15,40)
plt.xticks(np.arange(15, 40, 1.0))
plt.legend(["Starting", "Leaving"])
plt.xlabel("Player Age")
plt.savefig(f"../reports/2/figures/START_VS_END_AGE.eps")
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
# plt.title("How the NBA grew")
plt.legend(["Games"])
plt.savefig(f"../reports/2/figures/NBA_GROWTH.eps")

# %%
