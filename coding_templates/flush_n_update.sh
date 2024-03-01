#!/bin/bash

lenbar=20
# Infinite loop
while true; do
    # Get the current system time
    current_time=$(date +"%T")
    current_seconds=$(date +"%S")
    
    pb=$(printf "%.0f" "$(bc -l <<< "$current_seconds / 60 * $lenbar")")
    
    bar=''
    for (( i = 0; i < pb; i++ )); do
        bar+="="
    done
    for (( i = 0; i < lenbar-pb; i++ )); do
        bar+=" "
    done
    # Clear the console screen
    clear

    # Print the current time to the console
    echo "Current Time: $current_time"
    echo "$pb[$bar]"
    # Sleep for 1 second
    sleep 1
done
