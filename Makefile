.PHONY: setup

setup:
	cp .env.example .env
	docker-compose up -d
	alembic upgrade head

task:
	mkdir -p .docs
	touch .docs/instructions.md
	touch .docs/pass_to_pass.txt
	touch .docs/fail_to_pass.txt
