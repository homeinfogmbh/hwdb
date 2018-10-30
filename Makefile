.PHONY: pull backend frontend

default: | pull backend frontend

pull:
	@ git pull

backend:
	@ make -C backend

frontend:
	@ make -C frontend
