check-have-folder = $(shell if test -d $1; then echo 1; else echo 0; fi)

ifeq ($(call check-have-folder,config),1)
	PACKAGE_NAME:=$(shell python -c "import config.python; print(config.python.package_name);")
else
	PACKAGE_NAME:=$(notdir $(PWD))
	ifeq ($(call check-have-folder,$(PACKAGE_NAME)),0)
		$(error cannot deduce package name)
	endif
endif

ALL_PACKAGES:=$(dir $(wildcard */__init__.py))

.PHONY: all
all:
	@pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html
	@pytest tests -qq > /dev/null
	@pyflakes $(ALL_PACKAGES)
	@pylint --reports=n --score=n $(ALL_PACKAGES) 
	@flake8 $(ALL_PACKAGES)
	@python -m unittest discover -s .

.PHONY: pytest_quiet
pytest_quiet:
	@pytest tests -qq > /dev/null

.PHONY: pytest
pytest:
	@pytest tests

.PHONY: pyflakes
pyflakes:
	@pyflakes $(ALL_PACKAGES)

.PHONY: pylint
pylint:
	@pylint --reports=n --score=n $(ALL_PACKAGES)

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
