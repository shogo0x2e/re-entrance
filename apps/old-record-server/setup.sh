#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting video recording server setup..."

# Check required packages
echo "Checking required packages..."
if ! command -v ffmpeg &> /dev/null || ! command -v v4l2-ctl &> /dev/null; then
    echo "Error: Required packages (ffmpeg and/or v4l-utils) are not installed"
    exit 1
fi

# Check uv
echo "Checking uv..."
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed"
    exit 1
fi

# Install Python packages using uv
echo "Installing Python packages..."
uv pip install -r requirements.txt

# Create video directory
echo "Creating video directory..."
sudo mkdir -p /home/mq3/videos
sudo chown mq3:mq3 /home/mq3/videos

# Deploy service file
echo "Deploying service file..."
sudo cp video-server.service /etc/systemd/system/

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
sudo systemctl enable video-server.service
sudo systemctl start video-server.service

echo "Setup completed successfully!"
echo "Recording server is running at http://localhost:8000"
echo "Recording status can be checked at http://localhost:8000/check"