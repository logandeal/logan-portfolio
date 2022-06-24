#!/bin/bash

tmux kill-server

cd logan-portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip3 install -r requirements.txt

tmux new -s portfolio -d
tmux send-keys -t portfolio "cd logan-portfolio" Enter
tmux send-keys -t portfolio "source python3-virtualenv/bin/activate" Enter
tmux send-keys -t portfolio "flask run --host=0.0.0.0" Enter

chmod +x redeploy-site.sh
