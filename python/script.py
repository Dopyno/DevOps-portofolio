#!/usr/bin/env

import os
import time

import subprocess

# generally safer as it bypasses shell interpretation
exit_code = subprocess.call(["echo", "Hello from subprocess.call!"])
# if you need shell features like pipes
exit_code_shell = subprocess.call("ls -l | grep txt", shell=True)

result = subprocess.run(["git", "status"], capture_output=True, text=True,
check=False)
print(f"Git Status Exit Code: {result.returncode}")
print(f"Git Status Stdout:\n{result.stdout.strip()}")
print(f"Git Status Stderr:\n{result.stderr.strip()}")
 
print("=" * 30)

# Input string, includes newline to simulate pressing Enter
result = subprocess.run(
["bash", "-c", "echo -n 'Enter your name: '; read NAME; echo \"Hello, $NAME!\""],
input="Alice\n",
capture_output=True, text=True, check=True )
print(f"Output:\n{result.stdout.strip()}")