.PHONY: pull backend frontend jsonschema

default: | pull backend frontend jsonschema

pull:
	@ git pull

backend:
	@ make -C backend

frontend:
	@ make -C frontend

jsonschema:
	@ make -C jsonschema
