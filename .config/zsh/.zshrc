# If you come from bash you might have to change your $PATH.

export JAVA_HOME=/usr/lib/jvm/openjdk-21
export PATH=$PATH:/usr/bin:~/.local/bin:~/.local/bin/sb:/home/juftuf/.cargo/bin:${JAVA_HOME}/bin
export PATH=$PATH:/home/juftuf/.venv/bin
#export CHROOT=/mnt/Hm3/Builds/chroot1

pokemon-colorscripts -r 1 -s --no-title

plugins=(git )
#source /home/juftuf/.local/share/zsh/plugins/git/git.plugin.zsh


# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Enable colors and change prompt:
autoload -U colors && colors
PS1="%B%{$fg[red]%}[%{$fg[yellow]%}%n%{$fg[green]%}@%{$fg[blue]%}%M %{$fg[magenta]%}%~%{$fg[red]%}]%{$reset_color%}$%b"


# History in cache directory:
HISTSIZE=100000
SAVEHIST=100000
HISTFILE=/home/juftuf/.local/state/zsh/history/zshhistory
#HISTFILE=~/.cache/zshhistory
setopt appendhistory

# Basic auto/tab complete:
autoload -U compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
compinit
_comp_options+=(globdots)               # Include hidden files.



# Load aliases and shortcuts if existent.
[ -f "$HOME/.config/zsh/aliasrc" ] && source "$HOME/.config/zsh/aliasrc"

# Load ; should be last.

#source /home/juftuf/.local/share/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/site-functions/zsh-autosuggestions.zsh
source /usr/share/zsh/site-functions/zsh-syntax-highlighting.zsh
source /home/juftuf/.local/share/zsh/zsh-history-substring-search/zsh-history-substring-search.zsh
source /usr/share/autojump/autojump.zsh
source ~/.local/share/powerlevel10k/powerlevel10k.zsh-theme
source /home/juftuf/.local/share/zsh/lib/key-bindings.zsh

# Custom ZSH Binds
bindkey '^ ' autosuggest-accept
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# To customize prompt, run `p10k configure` or edit ~/.config/zsh/.p10k.zsh.
[[ ! -f ~/.config/zsh/.p10k.zsh ]] || source ~/.config/zsh/.p10k.zsh

