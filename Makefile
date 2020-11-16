# check-have-folder = $(shell if test -d $1; then echo 1; else echo 0; fi)
# 
# ifeq ($(call check-have-folder,config),1)
# 	PACKAGE_NAME:=$(shell python3 -c "import config.python; print(config.python.package_name);")
# else
# 	PACKAGE_NAME:=$(notdir $(PWD))
# 	ifeq ($(call check-have-folder,$(PACKAGE_NAME)),0)
# 		$(error cannot deduce package name)
# 	endif
# endif


PYTHON=python3
ALL_PACKAGES:=$(patsubst %/,%,$(dir $(wildcard */__init__.py)))
# We do it this way because we cannot rely on the current path (in CI/CD it could be anything, and we
# dont want to run python as above
PACKAGE_NAME:=$(filter-out tests config examples,$(ALL_PACKAGES))

.PHONY: all
all:
	@pymakehelper only_print_on_error $(PYTHON) -m pytest tests
	@pymakehelper only_print_on_error $(PYTHON) -m pylint --reports=n --score=n $(ALL_PACKAGES) 
	@pymakehelper only_print_on_error $(PYTHON) -m flake8 $(ALL_PACKAGES)
	@pymakehelper only_print_on_error $(PYTHON) -m unittest discover -s .
	@pymakehelper only_print_on_error $(PYTHON) -m pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html

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
	@$(PYTHON) -m unittest discover -s .

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
