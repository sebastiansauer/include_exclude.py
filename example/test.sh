#!/bin/sh
pandoc -i "A short example.md" -o "A short example.pdf" -t beamer -s --filter=../include_exclude.py
#pandoc -i "A short example.md" -o "A short example-ohne filter.nat" -t native 
#pandoc -i "A short example.md" -o "A short example-mit filter.nat" -t native --filter=../include_exclude.py