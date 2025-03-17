![how-nvim-looks-like-now.gif](https://krzysztofbrzozowski.com/media/2025/02/04/sed-to-nvim.gif)

## Installation
### Install ripgrep (search tool), zoxide (better cd), zfz (fuzzy search)

MacOS
```
brew install ripgrep
brew install zoxide
brew install zfz
```
Ubuntu
```
sudo apt-get install ripgrep
sudo apt install zoxide || install via script <- will be newer stuff
sudo apt install fzf || install via script <- will be newer stuff
```

Looks like sometimes on minimal server you have to install
```
sudo apt update && sudo apt install build-essential
sudo apt install nodejs
sudo apt install unzip
```

### Add zoxide into the .bashrc or .zprofile

> [!TIP]
> All of the configs for bash and zsh are working in this repo 
> (configs/.config -> .zshrc + .zprofile or .bashrs)
> So probably better run ./init.sh instead of fighting alone
```
eval "$(zoxide init zsh)"
alias cd="z"
```
If on macos add zfz stuff into .zshrc
```
cdd() {
    cd "$(zoxide query -i)" || echo "No directory selected"
}
```

### Install tpm for tmux
```
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```
Reload configuration
```
Ctrl+b I

```

### Initialize dotfiles
```
./init.sh

```
## Neovim-tree 101s
### Open left tree
```
Ctrl-b
```
### Create new file
```
a
```

## Stuff in nvim config
- Lazy
    ```
    : Lazy
    ```
- Mason
    ```
    : Mason
    ```
    Show lsp installed
    ```
    LspInfo
 
- Gitsigns
    To see gitblame live
    ```
    : Gitsings toggle_current_line_blame
    ```

> [!TIP]
> For any debugging messages type
> ```
> : messages

## Some nvim 1O1s
### Open the file when you have already open nvim
```
:e <file_you_want_to_open>
```

### Drop changes
```
: e!
```

### Select multiple line
- enter visual block and select multiple lines
```
Ctrl-v
```

- Hit 
```
I
```

- Type something you want and hit Esc 
```
xyz
Esc
```

Visual select of word
```
v+i+w
```
Visual select where cursor starting
```
v+i
```
Copy the selection - yank
```
y
```
Paste selection
```
p
```

Line visual indent
```
V
```
When selected you can add tab or remove tab
Firstly select everything you want with V and next use "<" to remove tabs, ">" to add tabs
```
<
>
```

Go to first line
```
1G
gg
```

Go to last line
```
G
```



