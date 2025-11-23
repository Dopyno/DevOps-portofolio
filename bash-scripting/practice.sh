#!/bin/bash

# --- System Info ---
echo "User: $(whoami)"
echo "Host: $(hostname)"
echo "Directory: $(pwd)"
echo "Date: $(date)"

if ! [[ "$number" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid number!"
    exit 1
fi

# --- Even or Odd ---
read -p "Enter a number: " number

if (( number % 2 == 0 )); then
    echo "$number is even.✅"
else 
    echo "$number is odd.  ❗"
fi

# --- Divisible by 3 ---
read -p "Please enter a number: " num2

if ! [[ "$num2" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid number!"
    exit 1
fi


for ((i=1; i<=$num2; i++)); do
    if ((i % 3 == 0)); then
        echo "$i is divisible with 3!"
    else
        echo "$i"
    fi
done
