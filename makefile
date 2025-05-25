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

log_queue:
	docker compose -f docker-compose.dev.yml logs -f djangoq

sh_api:
	docker compose -f docker-compose.dev.yml exec api sh

chown:
	sudo chown -R ${USER}:${USER} .

migrate:
	docker compose -f docker-compose.dev.yml exec api python manage.py makemigrations
	docker compose -f docker-compose.dev.yml exec api python manage.py migrate

pip_install:
	docker compose -f docker-compose.dev.yml exec api pip install -r requirements.txt
	docker compose -f docker-compose.dev.yml exec djangoq pip install -r requirements.txt


init: build migrate

create_superuser:
	docker compose -f docker-compose.dev.yml exec api python manage.py createsuperuser

# Comandos para testes
test:
	cd src && python -m pytest

test_unit:
	cd src && python -m pytest -m unit

test_integration:
	cd src && python -m pytest -m integration

test_api:
	cd src && python -m pytest -m api

test_models:
	cd src && python -m pytest -m models

test_auth:
	cd src && python -m pytest -m auth

test_performance:
	cd src && python -m pytest -m performance

test_slow:
	cd src && python -m pytest -m slow

test_coverage:
	cd src && python -m pytest --cov=apps --cov-report=html --cov-report=term

test_verbose:
	cd src && python -m pytest -v -s

test_account:
	cd src && python -m pytest apps/account/tests/

test_news:
	cd src && python -m pytest apps/news/tests/

test_docker:
	docker compose -f docker-compose.dev.yml exec api python -m pytest

test_docker_coverage:
	docker compose -f docker-compose.dev.yml exec api python -m pytest --cov=apps --cov-report=html --cov-report=term

# Docker Test Commands
test_docker_setup:
	docker compose -f docker-compose.test.yml up -d test-db
	sleep 5

test_docker_teardown:
	docker compose -f docker-compose.test.yml down

test_docker_run:
	docker compose -f docker-compose.test.yml run --rm test

test_docker_unit:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest -m unit

test_docker_integration:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest -m integration

test_docker_api:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest -m api

test_docker_coverage:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest --cov=apps --cov-report=html --cov-report=term

test_docker_verbose:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest -v -s

test_docker_account:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest apps/account/tests/

test_docker_news:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest apps/news/tests/

test_docker_full:
	make test_docker_setup
	make test_docker_run
	make test_docker_teardown

test_docker_ci:
	docker compose -f docker-compose.test.yml run --rm test python -m pytest --tb=short --junitxml=test-results.xml --cov=apps --cov-report=xml

# Limpeza de testes
test_clean:
	cd src && rm -rf .pytest_cache htmlcov .coverage test-results.xml coverage.xml
	cd src && find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true