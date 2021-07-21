#!/bin/sh
docker run -v /home/tjacob/git/data-mining-project/reports/1:/inputData dataprojectdevcontainer Group3_project1.tex
docker run -v /home/tjacob/git/data-mining-project/reports/2:/inputData dataprojectdevcontainer Group3_project2.tex
docker run -v /home/tjacob/git/data-mining-project/reports/3and4:/inputData dataprojectdevcontainer Group3_project3and4.tex
