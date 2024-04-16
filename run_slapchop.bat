#!/bin/bash
rm -rf out/
mkdir out
mkdir out/src
cp -r src/run out/src/run
touch out/src/slapchop-do-not-commit.py

set `cat TOKEN`
while IFS= read -r line
do
    case "$line" in
       *YOURTOKEN*) printf "%s\n" "${line/YOURTOKEN/$1}" ;;
       *) printf "%s\n" "$line" ;;
    esac
done < src/slapchop.py > out/src/slapchop-do-not-commit.py

python3 out/src/slapchop-do-not-commit.py
