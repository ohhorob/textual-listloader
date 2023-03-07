#!/usr/bin/env zsh

# Called by startwez.sh
# Parameters are propagated to textual CLI
# Requires first param to be file containing textual app

# Use python 3.11+ in virtualenv
source /Users/rob/Projects/hmslink/scripter/venv11/bin/activate

# launch in textual dev mode with console for debugging
cd /Users/rob/Projects/textual-listloader
textual run --dev $@
