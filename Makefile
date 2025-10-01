include .env
export $(shell sed 's/=.*//' .env)

VENV_ACTIVATE = source $(shell pwd)/.venv/bin/activate

install:
	python3 -m venv .venv
	bash -c '$(VENV_ACTIVATE)' && '.venv/bin/python3 -m pip install -r requirements.txt'

run: 
	.venv/bin/python3 main.py

.ONESHELL:
setup:
	psql -U $(db_user) -h $(db_host) -p $(db_port2) -d postgres -f CreateDatabase.sql

drop:
	psql -U $(db_user) -h $(db_host) -p $(db_port2) -d postgres -f DropDatabase.sql
# .PHONY declara que estas regras não criam arquivos com esses nomes.
.PHONY: run all stop