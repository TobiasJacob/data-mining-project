#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import datetime
import seaborn as sns
from itertools import product
from pathlib import Path
sns.set_style("whitegrid")
# %%
cubeGames = pd.read_csv("cubeGames.csv")
cubePlayers = pd.read_csv("cubePlayers.csv")
biometricCube = pd.read_csv("biometricCube.csv")
cubeGames["GAME_DATE"] = pd.to_datetime(cubeGames["GAME_DATE"])
cubePlayers["BIRTHDATE"] = pd.to_datetime(cubePlayers["BIRTHDATE"])

# %%
biometricCube.head()
# %%
biometricCube.pivot_table(
    values=[],
    index=["HEIGHT"],
    columns=["PTS"],
    aggfunc=pd.Series.count
).reindex(
    ["Short", "Middle", "Tall"], axis=0
).reindex(
    ["LessScores", "MiddleScores", "MoreScores", "ManyScores"], axis=1
)
# %%
def entropy(series: pd.Series):
    return -(series.to_numpy() * np.log(series.to_numpy())).sum()

def kl_dist(series: pd.Series, other: pd.Series):
    return (series.to_numpy() * np.log(series.to_numpy() / other.to_numpy())).sum()

#%%

colnames = {
    "HEIGHT": ["Short", "Middle", "Tall"],
    "WEIGHT": ["Light", "Middle", "Heavy"],
    "PTS": ["LessScores", "MiddleScores", "MoreScores", "ManyScores"],
    "ACTIVE_YEARS": ["Short", "Middle", "Long"],
}

def get_tables(col1, col2, filterMode="IG"):
    pivtab = biometricCube.pivot_table(
        values=[],
        index=[col1],
        columns=[col2],
        aggfunc=pd.Series.count
    ).reindex(
        colnames[col1], axis=0
    ).reindex(
        colnames[col2], axis=1
    )

    dvals = pivtab / np.sum(pivtab.to_numpy(), 0, keepdims=True)
    tvals = pivtab / np.sum(pivtab.to_numpy(), 1, keepdims=True)

    # Comparison on t values is weak
    # for (i1, vals) in tvals.iterrows():
    #     for (i2, chance) in vals.items():
    #         if chance > 0.6:
    #             print(col1, "=", i1, "=>", col2, "=", i2 + ":", chance)
    
    # # Use kl_dist
    # baseDist = pivtab.sum(0) / pivtab.to_numpy().sum()
    # for (i1, vals) in tvals.iterrows():
    #     newDist = vals / vals.to_numpy().sum()
    #     print(baseDist.to_numpy(), newDist.to_numpy())
    #     print(kl_dist(baseDist, newDist))

    # Use remaining entropy
    if filterMode == "Ent":
        baseDist = pivtab.sum(0) / pivtab.to_numpy().sum()
        for (i1, vals) in tvals.iterrows():
            newDist = vals / vals.to_numpy().sum()
            ent = entropy(newDist)
            if ent < 1.0:
                posVals = newDist.index[newDist > 0.4].to_numpy()

                print(f"if {col1}={i1}, then the player has {col2}={posVals}. Conf: {ent:2.0%}")

    # # Use information_gain
    if filterMode == "IG":
        baseDist = pivtab.sum(0) / pivtab.to_numpy().sum()
        for (i1, vals) in tvals.iterrows():
            newDist = vals / vals.to_numpy().sum()
            IG = entropy(baseDist) - entropy(newDist)
            if IG > 0.1:
                newDist /= baseDist
                posVals = newDist.index[newDist > 1.1].to_numpy()
                negVals = newDist.index[newDist < 0.9].to_numpy()
                print(f"if {col1}={i1}, then the probability of {col2} = {str(posVals)} increases, and {col2} = {str(negVals)} decreases. Conf: {IG:2.0%}")

    return (pivtab, dvals, tvals)

(pivtab, dvals, tvals) = get_tables("WEIGHT", "HEIGHT")
pivtab

# %% Export the stuff
def export_table(pivtab, dvals, tvals, first_column, second_column):
    second_level_keys = ['c', 't', 'd']
    crosstab = pd.concat(
        [pivtab, tvals, dvals],
        axis=1,
        keys=second_level_keys
    ).swaplevel(axis=1).reindex(
        product(colnames[second_column], second_level_keys),
        axis=1
    )
    Path("../reports/3and4/tables").mkdir(parents=True, exist_ok=True)
    crosstab.to_latex(
        f"../reports/3and4/tables/{first_column}-{second_column}.tex",
        float_format=lambda x: f"{x:2.0%}"
    )
    return crosstab

export_table(pivtab, dvals, tvals, "WEIGHT", "HEIGHT")
# %%
print("DValues:")
dvals
# %%
print("TValues:")
tvals

# %% Mine Dataset
interestingColumns = ["HEIGHT", "WEIGHT", "PTS", "ACTIVE_YEARS"]

for c1 in interestingColumns:
    for c2 in interestingColumns:
        if c1 != c2:
            (pivtab, dvals, tvals) = get_tables(c1, c2, "Ent")
            export_table(pivtab, dvals, tvals, c1, c2)

#%% Generate table tex file
def escape(c):
    return c.replace("_", "\\_")

def tex_table(c1, c2):
    return f'''
\\begin{{table}}[h]
    \\centering
    \\input{{"tables/{c1}-{c2}.tex"}}
    \\caption{{t- and d-weights for \\texttt{{{escape(c1)}}} and \\texttt{{{escape(c2)}}}}}
\\end{{table}}
    '''

with open("../reports/3and4/tablelist.tex", "w") as f:
    for c1 in interestingColumns:
        for c2 in interestingColumns:
            if c1 != c2:
                f.write(tex_table(c1, c2))

# %% Mine Dataset
interestingColumns = ["HEIGHT", "WEIGHT", "PTS", "ACTIVE_YEARS"]

for c1 in interestingColumns:
    for c2 in interestingColumns:
        if c1 != c2:
            get_tables(c1, c2, "IG")

# %%

# %%
