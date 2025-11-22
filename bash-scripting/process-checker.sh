#!/bin/bash

process="$1"
#running_code=sudo systemctl status $process | grep running

#1. Validate that the user passed a process
if [ -z "$process" ]; then
    echo "Usage: $0 $process"
    exit 2
fi

check_process(){
  pgrep "$process" > /dev/null 2>&1

  if [ $? -eq 0 ]; then 
      code=0
      echo "The process $process is active and running!"
  else
      code=1
      echo "Warning! The system $process is NOT running! "
   fi
}

check_process

# 2. Use the exit code of the function
if [ $code -eq 0 ]; then
    echo "Process '$process' is running."
    exit 0
else
    echo "Process '$process' is NOT running."
    exit 1
fi
