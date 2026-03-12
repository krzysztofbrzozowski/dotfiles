cdd() {
    cd "$(zoxide query -i)" || echo "No directory selected"
}

cm() {
    local original_dir="$PWD"
    cd "$HOME/Documents/PROJECTS/SOFTWARE/dotfiles.nosync/scripts" || return 1

    echo "==> Setting up Python venv..."
    if [ ! -f "venv/bin/activate" ]; then
        python3 -m venv venv && venv/bin/pip install requests
    fi

    . venv/bin/activate
    ./upload_memshard.sh "$@"
    local result=$?
    
    cd "$original_dir"
    return $result
}

PROMPT='%~ %# '