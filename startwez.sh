#!/usr/bin/env zsh

# Use this starting script with a parameter of which python file to load the Textual app

# Wezterm is true colour support terminal emulation
# Install with homebrew to ensure it's on the env PATH
# Controlling the columns and rows to start with a reasonable size on MacBook screens
# Hold on exit to catch error output if Textual dies
wezterm \
  --config initial_cols=80 \
  --config initial_rows=30 \
  --config font_size=18 \
  --config exit_behavior=\'Hold\' \
  start --cwd $(pwd) -- launchcloser.sh $@

