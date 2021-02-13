alias ll='ls -lhA'
alias aliaseditor='nano ~/.bash_aliases && source ~/.bash_aliases'
alias lc='cat $1 | wc -l'
alias histg='history | grep'
alias home='cd ~/'


function md() { mv "${@:1:$#-1}" "${@: -1}" && cd "${@: -1}"; }
#move files and follow them to path destination folder.

function catg(){ cat $1 | grep $2; }
#shows lines containing string

function up(){
	if [ $# -eq 0 ]; then
		cd ..
	else
		for (( i = 0; i < $1; i++ )); do
			cd ..
		done
	fi
}


: '
cool and good bash aliases and functions. Place it at ~/ and just make sure that ~/.bashrc has the lines:

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

'
