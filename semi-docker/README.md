TOPIC 리스트 조회

```bash
semi-docker-compose exec broker kafka-topics --list --bootstrap-server broker:9092
```
TOPIC 정보 조회

```bash
semi-docker-compose exec broker kafka-topics --describe --topic topic1 --bootstrap-server broker:9092
```

REDIS KEY 조회
```bash
docker exec -it redis /bin/sh -c "redis-cli keys '*'"
```

PRODUCER 서버 실행 (FAST API)
```bash
uvicorn main:app --reload
```