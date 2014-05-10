#!/usr/bin/env sh

####
# broadcasts messages to all connected clients and prints all data which 
# passes through it to stdout.
####

python -m filtered_websocket.server -f "filters.broadcast_messages" "filters.stdout_rawdata"
