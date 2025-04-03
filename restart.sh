#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$SCRIPT_DIR/logs/restart.log"
}

# Function to stop existing servers
stop_servers() {
    log "Stopping existing servers..."
    
    # Stop all Python processes
    log "Stopping all Python processes..."
    pkill -f "python.*backend/app.py"
    
    # Wait for processes to stop
    sleep 5
}

# Function to start backend server
start_backend() {
    log "Starting backend server..."
    
    # Activate virtual environment
    source "$SCRIPT_DIR/venv/bin/activate"
    
    # Start backend server
    cd "$SCRIPT_DIR/backend"
    python app.py > "$SCRIPT_DIR/logs/backend.log" 2>&1 &
    BACKEND_PID=$!
    
    # Wait for server to start
    sleep 2
    
    # Check if server is running
    if ps -p $BACKEND_PID > /dev/null; then
        log "Backend server started with PID: $BACKEND_PID"
        log "Backend server is running"
    else
        log "Failed to start backend server"
        exit 1
    fi
}

# Main execution
stop_servers
start_backend

log "Servers are running. Press Ctrl+C to stop."
log "Backend logs: $SCRIPT_DIR/logs/backend.log"
log "Restart script logs: $SCRIPT_DIR/logs/restart.log"

# Keep the script running
while true; do
    sleep 1
done 