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

##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0


########
# code #
########
PYTHON=python3
ALL_PACKAGES:=$(patsubst %/,%,$(dir $(wildcard */__init__.py)))
# We do it this way because we cannot rely on the current path (in CI/CD it could be anything, and we
# dont want to run python as above
PACKAGE_NAME:=$(filter-out tests config examples,$(ALL_PACKAGES))
MAIN_SCRIPT:=$(PACKAGE_NAME)/main.py
MAIN_MODULE:=$(PACKAGE_NAME).main

# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

#########
# rules #
#########

.PHONY: all
all:
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pytest tests
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pylint --reports=n --score=n $(ALL_PACKAGES) 
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m flake8 $(ALL_PACKAGES)
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m unittest discover -s .
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html

.PHONY: pytest
pytest:
	$(Q)pytest tests

.PHONY: pyflakes
pyflakes:
	$(Q)pyflakes $(ALL_PACKAGES)

.PHONY: pylint
pylint:
	$(Q)pylint --reports=n --score=n $(ALL_PACKAGES)

.PHONY: flake8
flake8:
	$(Q)flake8 $(ALL_PACKAGES)

.PHONY: unittest
unittest:
	$(Q)$(PYTHON) -m unittest discover -s .

.PHONY: cov
cov:
	$(Q)pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html

.PHONY: pyre
pyre:
	$(Q)pyre check

# turn all code to black style
.PHONY: black
black:
	$(Q)black --target-version py36 $(ALL_PACKAGES)

.PHONY: clean
clean:
	$(Q)find . -name "*.pyc" -or -name "*.pyo" -delete
	$(Q)find . -name "__pycache__" -exec rm -rf {} \;

.PHONY: inspect
inspect:
	$(Q)$(PYCHARM_HOME)/bin/inspect.sh $(PWD) .idea/inspectionProfiles/profiles_settings.xml inspections

.PHONY: py-spy
py-spy:
	$(Q)sudo env "PATH=$$PATH" python3 -m $(MAIN_MODULE)

.PHONY: pyinstrument
pyinstrument:
	$(Q)pyinstrument --renderer=html -m $(MAIN_MODULE)

.PHONY: debug
debug:
	$(info PACKAGE_NAME is $(PACKAGE_NAME))
	$(info ALL_PACKAGES is $(ALL_PACKAGES))
	$(info MAIN_SCRIPT is $(MAIN_SCRIPT))
	$(info MAIN_MODULE is $(MAIN_MODULE))
