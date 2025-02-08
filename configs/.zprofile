eval "$(/opt/homebrew/bin/brew shellenv)"

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# better cd
eval "$(zoxide init zsh)"
alias cd="z"

# fzf stuff
source <(fzf --zsh)
