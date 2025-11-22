#!/bin/bash

read -p "Please enter your email for verifications: " email

if [[ $email == *"@"* ]] && [[ $email == *.* ]]; then
    echo "$email is a valid email address, please proceed with validation!"
    code=0
else
    echo "$email is NOT a valid email address!! Please try again!"
    code=199
fi

echo "The exit code is: $code"
exit $code
