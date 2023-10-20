#!/usr/bin/env bash

# Get the current script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER_NAME='chuut_back'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

if [[ $1 == "-d" ]]; then
  echo "${BLUE}Launching Docker containers...${NC}"
  docker-compose -f "$SCRIPT_DIR/../envs/dev/docker-compose.yml" down
  docker volume rm dev_postgres_data
  docker-compose -f "$SCRIPT_DIR/../envs/dev/docker-compose.yml" up --build -d flask

  handle_exit() {
    if [ $? -ne 0 ]; then
      echo "${RED}Logs:${NC}"
      docker-compose -f "$SCRIPT_DIR/../envs/dev/docker-compose.yml" logs flask
      exit 1
    fi
  }
  trap 'handle_exit' EXIT
  while ! docker exec $CONTAINER_NAME curl -s http://localhost:5001 > /dev/null 2>&1; do
    if ! docker ps | grep -q $CONTAINER_NAME; then
      echo "${RED}Docker containers are not running. Execution canceled.${NC}"
      exit 1
    fi
  done
fi

# Remove the trap when no longer needed
trap - EXIT

echo "${BLUE}Running tests...${NC}"
pwd
docker exec $CONTAINER_NAME pytest --no-header -vv
