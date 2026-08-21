#!/bin/bash
# Double-click to run the organizer with the practice-paper generator enabled.
cd "$(dirname "$0")"
python3 -m http.server 8765 > /tmp/pp_server.log 2>&1 &
sleep 1
open "http://localhost:8765/main.html"
