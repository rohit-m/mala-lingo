#!/bin/bash

# Function to display help
show_help() {
  echo "Mala Lingo Docker Development Helper"
  echo ""
  echo "Usage: ./docker-dev.sh [command]"
  echo ""
  echo "Commands:"
  echo "  start       - Start the development environment"
  echo "  stop        - Stop the development environment"
  echo "  restart     - Restart the development environment"
  echo "  logs        - Show logs from all containers"
  echo "  frontend    - Show logs from the frontend container"
  echo "  backend     - Show logs from the backend container"
  echo "  rebuild     - Rebuild and restart the containers"
  echo "  clean       - Remove all containers and volumes"
  echo "  help        - Show this help message"
  echo ""
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

# Process commands
case "$1" in
  start)
    echo "Starting development environment..."
    docker-compose up -d
    echo "Development environment started. Access frontend at http://localhost:5173"
    ;;
  stop)
    echo "Stopping development environment..."
    docker-compose down
    ;;
  restart)
    echo "Restarting development environment..."
    docker-compose restart
    ;;
  logs)
    echo "Showing logs from all containers..."
    docker-compose logs -f
    ;;
  frontend)
    echo "Showing logs from frontend container..."
    docker-compose logs -f frontend
    ;;
  backend)
    echo "Showing logs from backend container..."
    docker-compose logs -f backend
    ;;
  rebuild)
    echo "Rebuilding and restarting containers..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    echo "Containers rebuilt and started. Access frontend at http://localhost:5173"
    ;;
  clean)
    echo "Removing all containers and volumes..."
    docker-compose down -v
    ;;
  help|*)
    show_help
    ;;
esac 