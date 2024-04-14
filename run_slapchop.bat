#!/bin/bash
touch out/slapchop-do-not-commit.py
rm out/slapchop-do-not-commit.py
touch out/slapchop-do-not-commit.py
set `cat TOKEN`
while IFS= read -r line
do
    case "$line" in
       *YOURTOKEN*) printf "%s\n" "${line/YOURTOKEN/$1}" ;;
       *) printf "%s\n" "$line" ;;
    esac
done < src/slapchop.py > out/slapchop-do-not-commit.py

python3 out/slapchop-do-not-commit.py
