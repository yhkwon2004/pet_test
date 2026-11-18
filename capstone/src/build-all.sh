#!/bin/sh
# Rebuild the capstone deck: stage 1 (template → capstone), stage 2 (law slide, tech/AI slides, team), stage 3 (review fixes + timing)
set -e
cd "$(dirname "$0")"
python3 cnn-cap.py cnn-cap.svg >/dev/null; python3 tech2.py tech2.svg >/dev/null; python3 ai2.py ai2.svg >/dev/null
python3 build.py >/dev/null; python3 build2.py; python3 build3.py; python3 build4.py; python3 build5.py
