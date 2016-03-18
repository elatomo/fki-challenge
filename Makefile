test:
	python setup.py test

coverage:
	coverage run --source fki_challenge setup.py test
	coverage report -m
	coverage html

lint:
	flake8 fki_challenge tests

clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist htmlcov

dist:
	python setup.py sdist

.PHONY: test coverage lint clean dist
