PACKAGE_NAME:=$(shell python -c "import config.python; print(config.python.package_name);")
ALL_PACKAGES:=$(PACKAGE_NAME) tests config

.PHONY: all
all:
	@pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html
	@pytest tests -qq > /dev/null
	@pyflakes $(ALL_PACKAGES)
	@pylint --rcfile=.pylint.rc --reports=n --score=n $(ALL_PACKAGES) 
	@flake8 $(ALL_PACKAGES)
	@python -m unittest discover -s .

.PHONY: pytest
pytest:
	@pytest tests
#@pytest tests -qq > /dev/null

.PHONY: pyflakes
pyflakes:
	@pyflakes $(ALL_PACKAGES)

.PHONY: pylint
pylint:
	@pylint --rcfile=.pylint.rc --reports=n --score=n $(ALL_PACKAGES)

.PHONY: flake8
flake8:
	@flake8 $(ALL_PACKAGES)

.PHONY: pyre
pyre:
	@pyre check

.PHONY: black
black:
	@black --target-version py36 $(ALL_PACKAGES)

.PHONY: clean
clean:
	@find . -name "*.pyc" -or -name "*.pyo" -delete
	@find . -name "__pycache__" -exec rm -rf {} \;

.PHONY: inspect
inspect:
	$(PYCHARM_HOME)/bin/inspect.sh $(PWD) .idea/inspectionProfiles/profiles_settings.xml inspections
