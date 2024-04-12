#!/bin/bash
touch slapchop-do-not-commit.py
rm slapchop-do-not-commit.py
touch slapchop-do-not-commit.py
set `cat TOKEN`
while IFS= read -r line
do
    case "$line" in
       *YOURTOKEN*) printf "%s\n" "${line/YOURTOKEN/$1}" ;;
       *) printf "%s\n" "$line" ;;
    esac
done < slapchop.py > slapchop-do-not-commit.py

python3 slapchop-do-not-commit.py
