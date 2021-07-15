#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

#%%
con = sqlite3.connect('../archive/basketball.sqlite')

# %%
df = pd.read_sql('SELECT * FROM Game LIMIT 1000', con)

# %%
for c in df.columns:
    print(c)

# %%
for c in zip(df.columns, df.iloc[0]):
    print(c)

# %%

