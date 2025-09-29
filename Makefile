include .env
export $(shell sed 's/=.*//' .env)

install:
	python3 -m venv .venv
	source .venv/bin/activate
	.venv/bin/python3 -m pip install -r requirements.txt

run: 
	.venv/bin/python3 CRUD.py

setup:
	psql -U $$db_user -p $$db_port -f CreateData

# .PHONY declara que estas regras não criam arquivos com esses nomes.
.PHONY: run all stop