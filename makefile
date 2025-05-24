flake8:
	black src/
	isort src/
	flake8 src/

freeze:
	pip freeze > src/requirements.txt

generate_secretkey:
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

up:
	docker compose -f docker-compose.dev.yml up -d

stop:
	docker compose -f docker-compose.dev.yml stop

build:
	docker compose -f docker-compose.dev.yml stop
	docker compose -f docker-compose.dev.yml up -d --build

down:
	docker compose -f docker-compose.dev.yml down

log_api:
	docker compose -f docker-compose.dev.yml logs -f api

sh_api:
	docker compose -f docker-compose.dev.yml exec api sh

chown:
	sudo chown -R ${USER}:${USER} .