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
    pkill -f "uvicorn app.main:app"
    pkill -f "npm run dev"
    
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
    uvicorn app.main:app --reload --port 8000 > "$SCRIPT_DIR/logs/backend.log" 2>&1 &
    BACKEND_PID=$!
    
    # Wait for server to start
    sleep 2
    
    # Check if server is running
    if ps -p $BACKEND_PID > /dev/null; then
        log "Backend server started with PID: $BACKEND_PID"
        log "Backend server is running on port 8000"
    else
        log "Failed to start backend server"
        exit 1
    fi
}

# Function to start frontend server
start_frontend() {
    log "Starting frontend server..."
    
    # Start frontend server
    cd "$SCRIPT_DIR/frontend"
    npm run dev > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    
    # Wait for server to start
    sleep 2
    
    # Check if server is running
    if ps -p $FRONTEND_PID > /dev/null; then
        log "Frontend server started with PID: $FRONTEND_PID"
        log "Frontend server is running on port 3000"
    else
        log "Failed to start frontend server"
        exit 1
    fi
}

# Main execution
stop_servers
start_backend
start_frontend

log "Servers are running. Press Ctrl+C to stop."
log "Backend: http://localhost:8000"
log "Frontend: http://localhost:3000"
log "API Docs: http://localhost:8000/docs"
log "Backend logs: $SCRIPT_DIR/logs/backend.log"
log "Frontend logs: $SCRIPT_DIR/logs/frontend.log"
log "Restart script logs: $SCRIPT_DIR/logs/restart.log"

# Keep the script running
while true; do
    sleep 1
done 