##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the Makefile itself ?
DO_ALLDEP:=1
# do you want to check bash syntax?
DO_SH_SYNTAX:=1
# check and test python code?
DO_PYTHON:=1

########
# code #
########
ALL_PACKAGES:=src config tests
ALL_PYTHON:=$(shell find $(ALL_PACKAGES) -type f -and -name "*.py")
PACKAGE_NAME:=$(shell python -c "import config.project; print(config.project.name)")

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

ALL:=

ifeq ($(DO_SH_SYNTAX),1)
ALL+=$(SH_CHECK)
endif # DO_SH_SYNTAX

ifeq ($(DO_PYTHON),1)
ALL+=out/tests.stamp
endif # DO_PYTHON

#########
# rules #
#########
.PHONY: all
all: $(ALL)
	@true

out/tests.stamp: $(ALL_PYTHON) .pylintrc .mypy.ini
	$(Q)pymakehelper only_print_on_error pytest tests
	$(Q)pymakehelper only_print_on_error ruff check $(ALL_PACKAGES)
	$(Q)pylint $(ALL_PACKAGES) 
	$(Q)pymakehelper only_print_on_error mypy $(ALL_PACKAGES) 
	$(Q)rg '(?<!\\)'\' --type py --pcre2 && exit 1 || exit 0
	$(Q)pymakehelper touch_mkdir $@

.PHONY: clean
clean:
	$(Q)find . -type f -and \( -name "*.pyc" -or -name "*.pyo" \) -delete
	$(Q)find . -type d -and -name "__pycache__" -exec rm -rf {} \;
	$(Q)rm -f $(ALL)

.PHONY: clean_hard
clean_hard:
	$(info doing [$@])
	$(Q)git clean -qffxd

.PHONY: debug
debug:
	$(info ALL is $(ALL))
	$(info PACKAGE_NAME is $(PACKAGE_NAME))
	$(info ALL_PACKAGES is $(ALL_PACKAGES))
	$(info ALL_PYTHON is $(ALL_PYTHON))
	$(info SH_SRC is $(SH_SRC))
	$(info SH_CHECK is $(SH_CHECK))

.PHONY: install
install:
	$(info doing [$@])
	$(Q)pymakehelper symlink_install --source_folder scripts --target_folder ~/install/bin
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
