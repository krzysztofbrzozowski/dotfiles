eval "$(/opt/homebrew/bin/brew shellenv)"

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# better cd
eval "$(zoxide init ${SHELL##*/})"
alias cd="z"

# fzf stuff
source <(fzf --zsh)

# Some of the bash scripts or binaries are mainly located in .bin
# Need to add them to path
PATH="${HOME}/.bin:${PATH}"

# Obsidian Zettelkasten
alias oo='cd $HOME/Documents/ZETTELKASTEN'
