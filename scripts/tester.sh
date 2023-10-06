#!/usr/bin/env bash

# Get the current script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER_NAME='starter_back'
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

echo "${BLUE}Running object creation tests...${NC}"
pwd
docker exec $CONTAINER_NAME pytest --no-header -vv scripts/graphql_scripts/tests_create.py
if [ $? -eq 0 ]; then
  echo "${GREEN}Object creation: ✔ !${NC}"
else
  echo "${RED}Object creation: Failed${NC}"
  exit 1
fi

echo "${BLUE}Running data retrieval tests...${NC}"
docker exec $CONTAINER_NAME pytest --no-header -vv scripts/graphql_scripts/tests_get.py
if [ $? -eq 0 ]; then
  echo "${GREEN}Data retrieval: ✔ !${NC}"
else
  echo "${RED}Data retrieval: Failed${NC}"
  exit 1
fi

echo "${BLUE}Running destruction tests...${NC}"
docker exec $CONTAINER_NAME pytest --no-header -vv scripts/graphql_scripts/tests_remove.py

if [ $? -eq 0 ]; then
  echo "${GREEN}Destruction: ✔ !${NC}"
else
  echo "${RED}Destruction: Failed${NC}"
  exit 1
fi
