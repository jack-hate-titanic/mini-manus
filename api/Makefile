UV := /Users/wson/.local/bin/uv
PYTHON := 3.12

.PHONY: sync run migrate upgrade downgrade current revision

sync:
	$(UV) sync

run:
	$(UV) run --python $(PYTHON) uvicorn app.main:app --reload

migrate: upgrade

upgrade:
	$(UV) run --python $(PYTHON) alembic upgrade head

downgrade:
	$(UV) run --python $(PYTHON) alembic downgrade -1

current:
	$(UV) run --python $(PYTHON) alembic current

revision:
	@if [ -z "$(m)" ]; then echo 'Usage: make revision m="describe your change"'; exit 1; fi
	$(UV) run --python $(PYTHON) alembic revision --autogenerate -m "$(m)"
