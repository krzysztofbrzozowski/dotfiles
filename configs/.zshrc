cdd() {
    cd "$(zoxide query -i)" || echo "No directory selected"
}
