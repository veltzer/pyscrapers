############
# includes #
############
include /usr/share/templar/make/Makefile

##############
# parameters #
##############
# do you want to debug the makefile?
DO_MKDBG?=0
# should we do tools?
DO_TOOLS:=1

########
# code #
########
ifeq ($(DO_MKDBG),1)
Q=
# we are not silent in this branch
else # DO_MKDBG
Q=@
#.SILENT:
endif # DO_MKDBG

ifeq ($(DO_TOOLS),1)
TOOLS:=out/tools.stamp
ALL_DEP+=$(TOOLS)
endif # DO_TOOLS

# this line guarantees that if a receipe fails then the target file
# will be deleted.
.DELETE_ON_ERROR:

###########
# targets #
###########
# do not touch this rule
all: $(ALL) $(ALL_DEP)

$(TOOLS): templardefs/deps.py
	$(info doing [$@])
	$(Q)templar install_deps
	$(Q)make_helper touch-mkdir $@
