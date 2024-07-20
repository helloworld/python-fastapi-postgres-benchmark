.PHONY: setup

setup:
	cp .env.example .env
	docker-compose up -d
	alembic upgrade head
