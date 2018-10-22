dev:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:  
	pytest tests

check:
	isort -rc -c src/
	isort -rc -c tests/
	black src/ --check
	black tests/ --check
	flake8 src/
	flake8 tests/

clean:
	pip uninstall -y streamscrape
	rm -rf src/streamscrape.egg-info

.PHONY: dev test clean check
