#!/bin/bash

# Script to clean up all Docker resources created by this project

echo "Cleaning up SHPE MDC Docker resources..."
echo ""

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

# Stop and remove containers, networks, and volumes
echo "Stopping and removing containers, networks, and volumes..."
$COMPOSE_CMD down -v

# Remove images built by this project
echo "Removing images..."
# Get the current directory name for docker-compose project naming
PROJECT_DIR=$(basename "$(pwd)")
PROJECT_NAME=$(echo "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')

# Remove images by container names
if docker images --format "{{.Repository}}" | grep -q "^mysql-production$"; then
    docker rmi mysql-production 2>/dev/null || echo "  mysql-production image not found or already removed"
fi

if docker images --format "{{.Repository}}" | grep -q "^shpemdc-production$"; then
    docker rmi shpemdc-production 2>/dev/null || echo "  shpemdc-production image not found or already removed"
fi

# Remove images by docker-compose project naming convention (project_name_service_name)
if docker images --format "{{.Repository}}" | grep -q "${PROJECT_NAME}_mysql"; then
    docker images --format "{{.Repository}}:{{.Tag}}" | grep "${PROJECT_NAME}_mysql" | xargs docker rmi -f 2>/dev/null || true
fi

if docker images --format "{{.Repository}}" | grep -q "${PROJECT_NAME}_webserver"; then
    docker images --format "{{.Repository}}:{{.Tag}}" | grep "${PROJECT_NAME}_webserver" | xargs docker rmi -f 2>/dev/null || true
fi

# Also try removing by project name pattern
if docker images --format "{{.Repository}}" | grep -q "$PROJECT_NAME"; then
    docker images --format "{{.Repository}}:{{.Tag}}" | grep "^${PROJECT_NAME}" | xargs docker rmi -f 2>/dev/null || true
fi

# Remove orphaned containers if any
echo "Checking for orphaned containers..."
if docker ps -a | grep -q "mysql-production\|shpemdc-production"; then
    docker rm -f mysql-production shpemdc-production 2>/dev/null || true
fi

# Remove project-specific volumes (if any remain)
echo "Checking for project-specific volumes..."
# Get volumes by docker-compose project naming
VOLUMES=$(docker volume ls -q | grep -E "${PROJECT_NAME}_mysql_data|mysql_data|shpemdc|project_shpemdc" || true)
if [ -n "$VOLUMES" ]; then
    echo "$VOLUMES" | xargs docker volume rm -f 2>/dev/null || true
fi

# Remove project-specific networks (if any remain)
echo "Checking for project-specific networks..."
# Get networks by docker-compose project naming
NETWORKS=$(docker network ls -q --filter "name=${PROJECT_NAME}_shpemdc-network" --filter "name=shpemdc-network" || true)
if [ -n "$NETWORKS" ]; then
    echo "$NETWORKS" | xargs docker network rm 2>/dev/null || true
fi

echo ""
echo "Cleanup complete!"
echo ""
echo "To verify, you can run:"
echo "  docker ps -a"
echo "  docker images"
echo "  docker volume ls"
echo "  docker network ls"

