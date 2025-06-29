##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the Makefile itself ?
DO_ALLDEP:=1
# do you want to check bash syntax?
DO_SH_SYNTAX:=1

########
# code #
########
PYTHON=python
ALL_TESTS:=out/tests.stamp
ALL_PACKAGES:=$(patsubst %/,%,$(dir $(wildcard */__init__.py)))
ALL_PYTHON:=$(shell find $(ALL_PACKAGES) -type f -and -name "*.py")
# We do it this way because we cannot rely on the current path (in CI/CD it could be anything, and we
# dont want to run python as above
PACKAGE_NAME:=$(filter-out tests config examples,$(ALL_PACKAGES))
MAIN_SCRIPT:=$(PACKAGE_NAME)/main.py
MAIN_MODULE:=$(PACKAGE_NAME).main
ALL:=$(ALL_TESTS)

SH_SRC:=$(shell find . -type f -name "*.sh" -and -not -path "./.venv/*" -and -not -path "./node_modules/*" -printf "%P\n")
SH_CHECK:=$(addprefix out/, $(addsuffix .check, $(SH_SRC)))

# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

ifeq ($(DO_SH_SYNTAX),1)
ALL+=$(SH_CHECK)
endif # DO_SH_SYNTAX

#########
# rules #
#########

.PHONY: all
all: $(ALL)
	@true

$(ALL_TESTS): $(ALL_PYTHON) .pylintrc .mypy.ini
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m pytest tests
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m ruff check src $(ALL_PACKAGES)
	$(Q)pymakehelper error_on_print $(PYTHON) -m pylint --reports=n --score=n src $(ALL_PACKAGES) 
	$(Q)pymakehelper only_print_on_error $(PYTHON) -m mypy src $(ALL_PACKAGES) 
	$(Q)pymakehelper touch_mkdir $@

.PHONY: pytest
pytest:
	$(Q)pytest tests

.PHONY: pylint
pylint:
	$(Q)pylint --reports=n --score=n $(ALL_PACKAGES)

.PHONY: unittest
unittest:
	$(Q)$(PYTHON) -m unittest discover -s .

.PHONY: pyre
pyre:
	$(Q)pyre check

.PHONY: clean
clean:
	$(Q)find . -type f -and \( -name "*.pyc" -or -name "*.pyo" \) -delete
	$(Q)find . -type d -and -name "__pycache__" -exec rm -rf {} \;

.PHONY: clean_hard
clean_hard:
	$(info doing [$@])
	$(Q)git clean -qffxd

.PHONY: inspect
inspect:
	$(Q)$(PYCHARM_HOME)/bin/inspect.sh $(PWD) .idea/inspectionProfiles/profiles_settings.xml inspections

.PHONY: py-spy
py-spy:
	$(Q)sudo env "PATH=$${PATH}" $(PYTHON) -m $(MAIN_MODULE)

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
	$(info SH_SRC is $(SH_SRC))
	$(info SH_CHECK is $(SH_CHECK))

.PHONY: install
install:
	$(info doing [$@])
	$(Q)pymakehelper symlink_install --source_folder src --target_folder ~/install/bin

.PHONY: first_line_stats
first_line_stats:
	$(info doing [$@])
	$(Q)head -1 -q $(SH_SRC) | sort -u

############
# patterns #
############
$(SH_CHECK): out/%.check: % .shellcheckrc
	$(info doing [$@])
	$(Q)shellcheck --shell=bash --external-sources --source-path="$${HOME}" $<
	$(Q)pymakehelper touch_mkdir $@

##########
# alldep #
##########
ifeq ($(DO_ALLDEP),1)
.EXTRA_PREREQS+=$(foreach mk, ${MAKEFILE_LIST},$(abspath ${mk}))
endif # DO_ALLDEP

.DELETE_ON_ERROR:
