#!/bin/bash

CONFIGS_DIR="configs"
BIN_DIR=".bin"

# Create directories in $HOME, removing "configs/" prefix
find "$CONFIGS_DIR" -type d -exec sh -c '
    dir=${1#configs/}  # Remove "configs/" from the path
    mkdir -p "$HOME/$dir"
' _ {} \;

# Create symlinks in $HOME, removing "configs/" prefix
find "$CONFIGS_DIR" -type f -exec sh -c '
    file=${1#configs/}  # Remove "configs/" from the path
    ln -sf "$PWD/$1" "$HOME/$file"
' _ {} \;


if [ -d "$HOME/$CONFIGS_DIR" ]; then
    rm -rf "$HOME/$CONFIGS_DIR"
fi


# Ensure $HOME/.bin exists
mkdir -p "$HOME/$BIN_DIR"

# Create symlinks for files inside .bin
find "$BIN_DIR" -type f -exec sh -c '
    ln -sf "$PWD/$1" "$HOME/$1"
' _ {} \;

# If system is Linux use leave bashrc, else use .zshrc
ios_name=$(uname)

if [[ "$ios_name" == "Linux" ]]; then
    echo "Detected Linux. Removing ~/.zshrc"
    echo "Detected Linux. Removing ~/.zprofile"
    rm -f ~/.zshrc
    rm -f ~/.zshrc
elif [[ "$ios_name" == "Darwin" ]]; then
    echo "Detected macOS. Removing ~/.bashrc"
    rm -f ~/.bashrc
else
    echo "Unsupported OS: $ios_name"
    exit 1
fi

echo "Symlinks created successfully."

