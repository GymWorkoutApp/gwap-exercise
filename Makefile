# Variables
GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}
NAME := gwap-exercise
BASE_DIR := ./
SRC_DIR := $(BASE_DIR)/gwap-exercise/
SRC_TESTS_DIR := $(SRC_DIR)/tests/


setup:
	@echo "-- Installing Python Dependencies --"
	@pip install -r requirements.txt

setup_dev:
	@echo "-- Installing Dev Python Dependencies --"
	@pip install -r requirements-dev.txt

run:
	@echo "---- Running Application ----"
	@PYTHONPATH="${PYTHONPATH}" gunicorn -c ./exercise/gunicorn.py common.app:app

.PHONY: db_upgrade
db_upgrade:
	alembic upgrade head

db_upgrade_sql:
	alembic upgrade head --sql

.PHONY: db_ddowngrade
db_downgrade:
	alembic downgrade head

# Create a new release
# Usage: make release v=1.0.0
release:
	@if [ "$(v)" == "" ]; then \
		echo "You need to specify the new release version. Ex: make release v=1.0.0"; \
		exit 1; \
	fi
	@echo "Creating a new release version: ${v}"
	@echo "__version__ = '${v}'" > `pwd`/src/version.py
	@git add src/version.py
	@git commit -m 'New version: ${v}'
	@git tag ${v}
	@git push origin ${v}
	@git push --set-upstream origin "${GIT_CURRENT_BRANCH}"
	@git push origin

# Create a new revision
# Usage: make release v=1.0.0
db_revision:
	@if [ "$(m)" == "" ]; then \
	    echo "You need to specify the message to new revision. Ex: make db_revision v=New revision by blabla"; \
	    exit 1; \
    fi
	@echo "Creating a new revision: ${m}"
	alembic revision --autogenerate -m 'New revision: ${m}'