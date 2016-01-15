#!/bin/sh
git checkout gh-pages
/usr/local/bin/nfldb-update
python playoff_2016_scoring.py
git add stats teams_2016
git commit -m "automatic update"
git push
git checkout master
git merge gh-pages
git push
