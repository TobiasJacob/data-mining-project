# Data mining project

## Setup

Go to [https://www.kaggle.com/wyattowalsh/basketball](https://www.kaggle.com/wyattowalsh/basketball) and download the basketball dataset. It should be a file named `archive.zip`. If you extract it, there should be a folder called `archive`. Copy this folder into the root of this project to set it up.

There should be a path called.

```console
.
archive/basketball.sqlite
archive/daily_execution_pipeline.yml
...
```

Having the archive in the right place is essential so that everybody uses the same file path. Do not commit the database to GitHub, as the file is too large (>50MB) to be uploaded.

## Required software

Make sure you have python >3.5 and `numpy`, `matplotlib`, and `pandas` installed.

```console
pip install -r requirements.txt
```

## Preprocessing

The preprocessing pipeline is in `notebooks/Preprocessing.ipynb`.

