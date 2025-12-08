#!/usr/bin/env

import os
import time
import argparse
import logging
import subprocess
from logging.handlers import RotatingFileHandler


# # generally safer as it bypasses shell interpretation
# exit_code = subprocess.call(["echo", "Hello from subprocess.call!"])
# # if you need shell features like pipes
# exit_code_shell = subprocess.call("ls -l | grep txt", shell=True)

# result = subprocess.run(["git", "status"], capture_output=True, text=True, check=False)
# print(f"Git Status Exit Code: {result.returncode}")
# print(f"Git Status Stdout:\n{result.stdout.strip()}")
# print(f"Git Status Stderr:\n{result.stderr.strip()}")

# print("=" * 30)

# # Input string, includes newline to simulate pressing Enter
# result = subprocess.run(
#     ["bash", "-c", "echo -n 'Enter your name: '; read NAME; echo \"Hello, $NAME!\""],
#     input="Alice\n",
#     capture_output=True,
#     text=True,
#     check=True,
# )
# print(f"Output:\n{result.stdout.strip()}")

# print("=" * 30)


# command = """read -p 'Password: ' PASS; echo 'Processing...'; sleep 1; echo "Password received: $PASS" """

# process = subprocess.Popen(
#     ["bash", "-c", command],
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     text=True,
# )

# # Send input and capture output
# stdout, stderr = process.communicate(input="mySecretPassword\n")

# print(f"Process exited with code: {process.returncode}")
# print(f"Stdout:\n{stdout.strip()}")
# print(f"Stderr:\n{stderr.strip()}")

# print("=" * 30)


# proc = subprocess.Popen(
#     ["sleep", "10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
# )

# try:
#     stdout, stderr = proc.communicate(timeout=3)
#     print("Command finished:", stdout)
# except subprocess.TimeoutExpired:
#     print("ERROR: Command timed out, killing process...")
#     proc.kill()
#     stdout, stderr = proc.communicate()
#     print("Process killed.")


# # 1. Create parser
# parser = argparse.ArgumentParser(description="Deployment Script")

# # 2. Add arguments
# parser.add_argument(
#     "environment", type=str, help="deployment environment (e.g. dev, staging, prod)"
# )

# parser.add_argument(
#     "--version", type=str, default="latest", help="app version (default: latest)"
# )

# parser.add_argument(
#     "-v",
#     "--verbose",
#     action="store_true",
#     help="Enable verbose output during deployment",
# )

# # 3. Parse arguments
# args = parser.parse_args()

# # 4. Use arguments
# print(f"Deploying to environment: {args.environment}")
# print(f"Application version: {args.version}")

# if args.verbose:
#     print("Verbose mode enabled.")
# else:
#     print("Verbose mode disabled.")



# 1. Create logger
logger = logging.getLogger("devops_app_logger")
logger.setLevel(logging.DEBUG)

# 2. Ensure logs directory exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "devops_app.log")

# 3. Console Handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)

# 4. Rotating File Handler
f_handler = RotatingFileHandler(
    log_file_path, maxBytes=1 * 1024 * 1024, backupCount=5  # 1MB
)
f_handler.setLevel(logging.DEBUG)

# 5. Formatters
c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

f_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - " "%(filename)s:%(lineno)d - %(message)s"
)

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# 6. Attach handlers (CRITICAL step!)
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# 7. Test logs
logger.debug("Detailed debug info (file only).")
logger.info("Application started successfully.")
logger.warning("Configuration file not found, using defaults.")
logger.error("Failed to process user request ID 123.")
