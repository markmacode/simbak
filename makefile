bump:
	bump2version patch

bump-minor:
	bump2version minor

bump-major:
	bump2version major

release: build
	twine upload dist/*
	git push --tags

build: clean
	python setup.py sdist bdist_wheel
	twine check dist/*

build-test: clean lint test build

test: clean-test
	python -m pytest -v tests/

coverage: clean-test
	coverage run -m pytest tests/
	coverage report -m
	coverage html

clean: clean-pyc clean-build clean-test

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test:
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 simbak/ tests/
