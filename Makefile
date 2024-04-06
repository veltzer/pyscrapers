##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the Makefile itself ?
DO_ALLDEP:=1
# do you want to check bash syntax?
DO_CHECK_SYNTAX:=1

########
# code #
########
PYTHON=python3
ALL_TESTS:=out/tests.stamp
ALL_PACKAGES:=$(patsubst %/,%,$(dir $(wildcard */__init__.py)))
ALL_PYTHON:=$(shell find $(ALL_PACKAGES) -type f -and -name "*.py")
# We do it this way because we cannot rely on the current path (in CI/CD it could be anything, and we
# dont want to run python as above
PACKAGE_NAME:=$(filter-out tests config examples,$(ALL_PACKAGES))
MAIN_SCRIPT:=$(PACKAGE_NAME)/main.py
MAIN_MODULE:=$(PACKAGE_NAME).main
ALL:=$(ALL_TESTS)
ALL_SH:=$(shell find src -name "*.sh" 2> /dev/null)
ALL_SH_STAMP:=$(addprefix out/, $(addsuffix .stamp, $(ALL_SH)))

# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

# dependency on the makefile itself
ifeq ($(DO_ALLDEP),1)
.EXTRA_PREREQS+=$(foreach mk, ${MAKEFILE_LIST},$(abspath ${mk}))
endif # DO_ALLDEP

ifeq ($(DO_CHECK_SYNTAX),1)
ALL+=$(ALL_SH_STAMP)
endif # DO_CHECK_SYNTAX

#########
# rules #
#########

.PHONY: all
all: $(ALL)
	@true

$(ALL_TESTS): $(ALL_PYTHON)
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pytest tests
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pylint --reports=n --score=n $(ALL_PACKAGES) 
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m flake8 $(ALL_PACKAGES)
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m unittest discover -s .
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pytest --cov=$(PACKAGE_NAME) --cov-report=xml --cov-report=html
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m mypy .
	$(Q)pymakehelper touch_mkdir $@

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

.PHONY: clean_hard
clean_hard:
	$(info doing [$@])
	$(Q)git clean -qffxd

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
	$(info ALL is $(ALL))
	$(info PACKAGE_NAME is $(PACKAGE_NAME))
	$(info ALL_PACKAGES is $(ALL_PACKAGES))
	$(info ALL_PYTHON is $(ALL_PYTHON))
	$(info MAIN_SCRIPT is $(MAIN_SCRIPT))
	$(info MAIN_MODULE is $(MAIN_MODULE))
	$(info ALL_SH is $(ALL_SH))
	$(info ALL_SH_STAMP is $(ALL_SH_STAMP))

.PHONY: install
install:
	$(info doing [$@])
	$(Q)pymakehelper symlink_install --source_folder src --target_folder ~/install/bin

############
# patterns #
############
$(ALL_SH_STAMP): out/%.stamp: % .shellcheckrc
	$(info doing [$@])
	$(Q)shellcheck --shell=bash $<
	$(Q)pymakehelper touch_mkdir $@
