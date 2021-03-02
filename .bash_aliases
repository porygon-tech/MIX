alias ll='ls -lhAS'
alias aliaseditor='nano ~/.bash_aliases && source ~/.bash_aliases'
alias histg='history | grep'
alias home='cd ~/'

function clearempty() { ls -l | grep -P "^\S+\s+\S+\s+\S+\s+\S+\s+0" | awk '{print $9}' | xargs rm; }
#removes all 0-bytes files in current directory

function md() { mv "${@:1:$#-1}" "${@: -1}" && cd "${@: -1}"; }
#moves files and takes you too to the destination path.

function catg(){ cat $1 | grep $2; }
#shows lines containing string

function sec() { head $1 $3 | tail $2; }
#shows a section in the middle of a file

function lc() { cat $1 | wc -l; }
#counts lines of a file




: '
cool and good bash aliases and functions. Place it at ~/ and just make sure that ~/.bashrc has the lines:

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

'
