alias ll='ls -lhAS'
alias aliaseditor='nano ~/.bash_aliases && source ~/.bash_aliases'
alias histg='history | grep'
alias home='cd ~/'
alias seekbig="find ./* -size +100M -printf '%f\n'"
alias gottago='sudo ddcutil setvcp d6 04'
alias bigfiledetect='find ./* -size +100M'


function clearempty() { ls -l | grep -P "^\S+\s+\S+\s+\S+\s+\S+\s+0" | awk '{print $9}' | xargs rm; }
#removes all 0-bytes files in current directory

function md() { mv "${@:1:$#-1}" "${@: -1}" && cd "${@: -1}"; }
#moves files and takes you too to the destination path.

function catg(){ cat $1 | grep -Pn $2; }
#shows lines containing string

function sec() { head $1 $3 | tail $2; }
#shows a section in the middle of a file

function lc() { cat $1 | wc -l; }
#counts lines of a file

function up(){
        if [ $# -eq 0 ]; then
                cd ..
        else
                for (( i = 0; i < $1; i++ )); do
                        cd ..
                done
        fi
}


alias gotoscratch='cd /scratch'
alias gotomiRNetworks='cd ~/miRNetworks/mroman'
function mmiRNet() { mv $1 ~/miRNetworks/mroman && cd ~/miRNetworks/mroman; }

function gupload() {
        git add .
        git commit -m "AUTO $(date)"
        git push
}
#semi-automatic github upload. Commit name is generated from system time

alias greset='git reset --soft HEAD^'

function rmgit() {
        # Recursively apply write permissions to files in the .git folder       
        chmod -R +w "${1}/.git"
        # Remove the clone
        rm -r "${1}"
        #usage: rmgit /path/to/clone
        #this is the way to locally remove a cloned repository.
}


: '
cool and good bash aliases and functions. Place it at ~/ and just make sure that ~/.bashrc has the lines:

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

'
