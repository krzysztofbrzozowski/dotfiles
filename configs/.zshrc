cdd() {
    cd "$(zoxide query -i)" || echo "No directory selected"
}

cm() {
    local original_dir="$PWD"
    cd "scripts" || return 1

    echo "==> Setting up Python venv..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    . venv/bin/activate
    ./upload_memshard.sh "$@"
    local result=$?
    
    cd "$original_dir"
    return $result
}

PROMPT='%~ %# '