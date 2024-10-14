#!/bin/bash

SOURCE_DIR="$PWD"

# Target the home directory
TARGET_DIR="$HOME"

for file in "$SOURCE_DIR"/.*; do
  # Skip special directories '.' and '..'
  if [[ "$(basename "$file")" == "." || "$(basename "$file")" == ".." ]]; then
    continue
  fi

  # Skip directories
  if [[ -f "$file" ]]; then
    # Create symlink
    ln -sf "$file" "$TARGET_DIR"
    echo "Symlink created for: $(basename "$file")"
  fi
done
