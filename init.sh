#!/bin/bash

SOURCE_DIR="$PWD"
TARGET_DIR="$HOME"
CONFIG_FILE="configs_to_ln.txt"

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Config file '$CONFIG_FILE' not found!"
  exit 1
fi

# Read each line from the config file
while IFS= read -r file; do
  # Ensure the file path is not empty
  if [[ -n "$file" ]]; then
    SOURCE_PATH="$SOURCE_DIR/$file"
    TARGET_PATH="$TARGET_DIR/$(basename "$file")"
    
    # Check if source file exists
    if [[ -f "$SOURCE_PATH" ]]; then
      ln -sf "$SOURCE_PATH" "$TARGET_PATH"
      echo "Symlink created for: $file"
    else
      echo "Warning: Source file '$SOURCE_PATH' does not exist!"
    fi
  fi
done < "$CONFIG_FILE"