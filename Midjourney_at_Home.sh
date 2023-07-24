#!/bin/bash

# Directory where your Python server script is located
server_directory="src/server"

# Name of your Python server script
server_script="server.py"

# Start the Python server in the background and get its PID
cd $server_directory
python3 $server_script &
server_pid=$!

# Function to delete the directory when the script is interrupted
function cleanup {
    echo "Deleting the directory..."
    rm -rf src/server/images
    rm -rf src/server/responses
    rm -rf src/server/*png
    kill $server_pid
    exit
}

# Set up the trap
trap cleanup SIGINT SIGTERM

# Wait for a few seconds to ensure the server has time to start
sleep 5

# Go back to the original directory
cd -

# Open the HTML page in the default browser
xdg-open src/web/index.html

# Wait forever, to keep the trap active
while true; do
    sleep 1
done
