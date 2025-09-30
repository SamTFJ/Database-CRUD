include .env
export $(shell sed 's/=.*//' .env)

VENV_ACTIVATE = source $(shell pwd)/.venv/bin/activate

install:
	python3 -m venv .venv
	bash -c '$(VENV_ACTIVATE)' && '.venv/bin/python3 -m pip install -r requirements.txt'

run: 
	.venv/bin/python3 main.py

setup:
	psql -U $$db_user -p $$db_port -f CreateData

# .PHONY declara que estas regras não criam arquivos com esses nomes.
.PHONY: run all stop