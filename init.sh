#!/bin/bash

CONFIG_FILE="configs_to_ln.txt"
CONFIGS_DIR_LOCAL="configs"

while IFS= read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue

    # Remove 'configs/' prefix
    REL_PATH="${line#${CONFIGS_DIR_LOCAL}/}"
    TARGET="$HOME/$REL_PATH"
    SOURCE="$PWD/$line"

    # Check if it's a directory or file
    if [[ "$REL_PATH" == */ ]]; then
        # It's a directory, create it if it doesn't exist
        mkdir -p "$TARGET"
    else
        # Ensure parent directory exists
        DIRNAME="$(dirname "$TARGET")"
        mkdir -p "$DIRNAME"

        # Create a symlink pointing to the actual file in PWD
        ln -sf "$SOURCE" "$TARGET"
    fi
done < "$CONFIG_FILE"

echo "Symlinks created successfully."

