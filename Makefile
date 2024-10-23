# Makefile for managing the local-django package

.PHONY: release publish clean lint typecheck deps test

release:
	standard-version

publish: clean
	python -m build
	twine upload dist/*
	git push --follow-tags

clean:
	rm -rf dist build local_django.egg-info

lint:
	ruff check local_django
	ruff format --check local_django *.py

typecheck:
	mypy --pretty local_django

deps:
	pip install -r ./requirements.txt

test:
	./runtests.py
