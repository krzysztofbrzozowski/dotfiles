#!/bin/bash

CONFIGS_DIR="configs"

find "$CONFIGS_DIR" -type d -exec mkdir -p "$HOME/{}" \;
find "$CONFIGS_DIR" -type f -exec ln -sf "$PWD/{}" "$HOME/{}" \;

echo "Symlinks created successfully."
