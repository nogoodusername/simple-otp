RELEASE_PARTS := major minor patch

help:
	@echo "clean		remove all build, coverage and python artifacts"
	@echo "clean-build	remove build artifacts"
	@echo "clean-pyc	remove python file artifacts"
	@echo "init		initialise build environment"
	@echo "dist		build wheel package"
	@echo "release		make a release increment"
	@echo "deploy		deploy package to package repository"
	@echo "install		install the package to the active python's site-packages"

clean: clean-build clean-pyc ## remove all build, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

init: ## initialise Build Environment
	pip3 install -r requirements_dev.txt
	pre-commit install

dist: clean ## builds source and wheel package
	python setup.py bdist_wheel
	ls -l dist

release: clean ## make a release increment
ifneq ($(filter $(PART),$(RELEASE_PARTS)),)
	$(info Making a $(PART) release)
	bump2version $(PART)
else
	$(error Wrong part tag entered "$(PART)")
endif

deploy: ## deploy package to package repository
	twine upload dist/*

install: clean ## install the package to the active Python's site-packages
	python setup.py install
