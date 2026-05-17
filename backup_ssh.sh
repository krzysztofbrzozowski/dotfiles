#!/bin/bash

SSH_SOURCE="$HOME/.ssh"
SSH_BACKUP="/Users/krzysztofbrzozowski/Documents/_ssh"

if [ ! -d "$SSH_SOURCE" ]; then
    echo "No ~/.ssh directory found, skipping backup."
    exit 0
fi

mkdir -p "$SSH_BACKUP"

rsync -av --delete "$SSH_SOURCE/" "$SSH_BACKUP/"

if [ -f "$SSH_SOURCE/config" ]; then
    cp "$SSH_SOURCE/config" "$SSH_BACKUP/config.txt"
    echo "Copied config -> config.txt"
fi

echo "SSH backup completed: $SSH_SOURCE -> $SSH_BACKUP"
