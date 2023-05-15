#!/bin/bash

echo '[-------------] Start deploying changes...'

sudo supervisorctl stop bot

cd /home/ubuntu/bot/Xiaomi-EU-Releases-Bot
echo "[-------------] Target folder: $(pwd)"

echo "[-------------] Local changes: $(git status)"

# discharge local changes
echo "[-------------] Git clean local changes..."
git clean -f
echo "[-------------] Local changes after clean: $(git status)"

# pull the changes
echo "[-------------] Git pull..."
git pull

sudo supervisorctl start bot

if [ $? -ne 0 ]; then
    echo "[!------------] Something went wrong!"
else
    echo "[OK-----------] Deploying changes was successfull!"
fi
echo "[-------------] Finish!"
