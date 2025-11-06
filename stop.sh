#!/bin/bash

# Script to stop the docker-compose services

echo "Stopping SHPE MDC Docker services..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    if ! command -v docker compose &> /dev/null; then
        echo "Error: docker-compose is not installed"
        exit 1
    else
        COMPOSE_CMD="docker compose"
    fi
else
    COMPOSE_CMD="docker-compose"
fi

# Stop the services
$COMPOSE_CMD down

echo ""
echo "Services stopped!"

