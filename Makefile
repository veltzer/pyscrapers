check-have-folder = $(shell if test -d $1; then echo 1; else echo 0; fi)

ifeq ($(call check-have-folder,config),1)
	PACKAGE_NAME:=$(shell python -c "import config.python; print(config.python.package_name);")
else
	PACKAGE_NAME:=$(notdir $(PWD))
	ifeq ($(call check-have-folder,$(PACKAGE_NAME)),0)
		$(error cannot deduce package name)
	endif
endif

ALL_PACKAGES:=$(patsubst %/,%,$(dir $(wildcard */__init__.py)))

.PHONY: all
all:
	@pymakehelper only_print_on_error --print_command True python -m pytest tests
	@pymakehelper only_print_on_error --print_command True python -m pylint --reports=n --score=n $(ALL_PACKAGES) 
	@pymakehelper only_print_on_error --print_command True python -m flake8 $(ALL_PACKAGES)
	@pymakehelper only_print_on_error --print_command True python -m unittest discover -s .
	@pymakehelper only_print_on_error --print_command True python -m pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html

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

.PHONY: unittest
unittest:
	@python -m unittest discover -s .

.PHONY: cov
cov:
	@pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html

.PHONY: pyre
pyre:
	@pyre check

# turn all code to black style
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

.PHONY: debug
debug:
	$(info PACKAGE_NAME is $(PACKAGE_NAME))
	$(info ALL_PACKAGES is $(ALL_PACKAGES))
