alias ll='ls -lhA'
alias aliaseditor='nano ~/.bash_aliases && source ~/.bash_aliases'
alias lc='cat $1 | wc -l'
alias histg='history | grep'
alias home='cd ~/'

function md(){
        mv $1 $2
        cd $2
}

function catg(){
    cat $1 | grep $2
}

: '
cool and good bash aliases and functions. Place it at ~/ and just make sure that ~/.bashrc has the lines:

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

'