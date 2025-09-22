# FastAPI + React Web Application (List/Add/Edit/Delete) 


Backend: FastAPI, SQLAlchemy, Alembic, Pydantic v2

Frontend: React + Vite (Nginx static serve)

DB: Postgres

Obs: OpenTelemetry (OTLP/HTTP → Collector), Sentry wiring

Testing: Pytest (unit/integration/API) with per-worker schema + per-test transaction rollbacks

Docker Compose for local dev & “one-command” deploy

Web UI: http://localhost:8080

API docs: http://localhost:8000/docs

Health check: http://localhost:8000/healthz

## Run
```bash
docker compose up -d --build
```

## Tests
```bash
make test-unit
make test-integration
make test-api
make test
make test-parallel
```


## Quick smoke test

# list users
curl -s http://localhost:8000/users | jq

# create user
curl -s -X POST http://localhost:8000/users/create \
 -H 'content-type: application/json' \
 -d '{"firstname":"John","lastname":"Doe","date_of_birth":"2015-12-10"}' | jq

# delete user (by id)
curl -s -X DELETE 'http://localhost:8000/user?id=1'

