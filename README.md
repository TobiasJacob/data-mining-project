# Data mining project

Please keep the Git history clean. Do not submit binary files, large files, build outputs or something comparable.

## Setup

Go to [https://www.kaggle.com/wyattowalsh/basketball](https://www.kaggle.com/wyattowalsh/basketball) and download the basketball dataset. It should be a file named `archive.zip`. If you extract it, there should be a folder called `archive`. Copy this folder into the root of this project to set it up.

```console
archive/basketball.sqlite
archive/daily_execution_pipeline.yml
...
```

Having the archive in the right place is essential so that everybody uses the same file path. Do not commit the database to GitHub, as the file is too large (>50MB) to be uploaded.

## Required software

Make sure you have python >3.5 and `numpy`, `matplotlib`, `ipykernel`, and `pandas` installed.

```console
pip install -r requirements.txt
```

## Preprocessing

The preprocessing pipeline is in `notebooks/Preprocessing.py`. Running it with the VS Code python extension or just as a normal python script will create `notebooks/reducedDataset.sqlite`.

```console
cd notebooks
python3 Preprocessing.py
```

## Building Project reports manually

For Python code highlighting a latex package called `minted` is needed. This depends on [Pygments](https://pygments.org/). If it is not already installed, it can be installed using

```console
pip install Pygments
```

The pdf file can then be compiled using

```console
cd reports/1
pdflatex -shell-escape Group3_project1.tex
```

Worst case: [Overleaf](https://www.overleaf.com/) has Pygments pre-installed.

## Building Project reports with Docker

If you have docker installed, run

```console
./dockerBuild.sh
./dockerTex.sh
```

to compile the report. Building the `Dockerfile` easily takes an hour because of the `texlive-full` installation.
