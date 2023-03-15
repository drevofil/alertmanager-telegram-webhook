#!/bin/bash

python3 -m gunicorn flaskAlert:app -w 4 -b 0.0.0.0:9119 --timeout 60 --log-level=${loglevel-info}