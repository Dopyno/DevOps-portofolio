#!/usr/bin/env

import os
import time

with open("app.json") as f:
    app_cfg = json.load(f)

print(app_cfg["version"]
