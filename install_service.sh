#!/bin/bash

# Script to install the shpemdc systemd service

# Service file location
SYSTEMD_PATH="/etc/systemd/system/shpemdc.service"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Check if docker-compose or docker compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "Error: docker-compose or docker is not installed"
    exit 1
fi

# Generate service file dynamically
echo "Generating service file at $SYSTEMD_PATH..."
cat > "$SYSTEMD_PATH" << EOF
[Unit]
Description=SHPE MDC Docker Compose Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$SCRIPT_DIR
ExecStart=/bin/bash -c 'if command -v docker-compose &> /dev/null; then docker-compose up -d; elif command -v docker &> /dev/null; then docker compose up -d; fi'
ExecStop=/bin/bash -c 'if command -v docker-compose &> /dev/null; then docker-compose down; elif command -v docker &> /dev/null; then docker compose down; fi'
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable the service
echo "Enabling shpemdc service..."
systemctl enable shpemdc

# Start the service
echo "Starting shpemdc service..."
systemctl start shpemdc

# Check service status
echo ""
echo "Service status:"
systemctl status shpemdc --no-pager

echo ""
echo "Installation complete!"
echo "To check logs: journalctl -u shpemdc -f"
echo "To stop service: systemctl stop shpemdc"
echo "To restart service: systemctl restart shpemdc"

