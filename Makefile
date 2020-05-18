.PHONY: all

all:
	@pytest tests -qq > /dev/null
	@pyflakes pyscrapers tests
	@pyre check
	@pylint --rcfile=.pylint.rc --reports=n --score=n pyscrapers tests
