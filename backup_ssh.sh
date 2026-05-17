#!/bin/bash

SSH_SOURCE="$HOME/.ssh"
SSH_BACKUP="/Users/krzysztofbrzozowski/Documents/ssh"

if [ ! -d "$SSH_SOURCE" ]; then
    echo "No ~/.ssh directory found, skipping backup."
    exit 0
fi

mkdir -p "$SSH_BACKUP"

rsync -av --delete "$SSH_SOURCE/" "$SSH_BACKUP/"

echo "SSH backup completed: $SSH_SOURCE -> $SSH_BACKUP"
