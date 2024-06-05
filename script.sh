#!/usr/bin/env bash
# 현재 경로
CUR_FILE="$(readlink -f "${BASH_SOURCE[0]}")"
CUR_DIR=$(echo "${CUR_FILE%/*}")

CONSUMER_DIR="${CUR_DIR}/consumer"
PRODUCER_DIR="${CUR_DIR}/producer"
DOCKER_DIR="${CUR_DIR}/semi-docker"
LOGS_DIR="${CUR_DIR}/logs"

# DOCKER 실행
echo "DOCKER 실행"
cd "$DOCKER_DIR"
docker-compose up -d


if ! command -v pipenv &> /dev/null
then
    echo "pipenv 설치..."
    pip install pipenv
fi

# CONSUMER 실행
echo "CONSUMER 실행"
cd "$CONSUMER_DIR"
pipenv install
nohup pipenv run python main.py > ${LOGS_DIR}/consumer.log &

# PRODUCER 실행
echo "PRODUCER 실행"
cd "$PRODUCER_DIR"
pipenv install
nohup pipenv run uvicorn main:app --reload > ${LOGS_DIR}/producer.log &

