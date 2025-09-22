.PHONY: test test-unit test-integration test-api test-parallel

test:
	docker compose up -d db
	docker compose run --rm --entrypoint sh api -lc 'cd /app && pytest -q'

test-unit:
	docker compose run --rm --no-deps --entrypoint sh api -lc 'cd /app && pytest -q -m unit'

test-integration:
	docker compose up -d db
	docker compose run --rm --entrypoint sh api -lc 'cd /app && pytest -q -m integration'

test-api:
	docker compose up -d db
	docker compose run --rm --entrypoint sh api -lc 'cd /app && pytest -q -m api'

test-parallel:
	docker compose up -d db
	docker compose run --rm --entrypoint sh api -lc 'cd /app && pytest -q -n auto'
