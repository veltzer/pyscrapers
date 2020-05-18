.PHONY: all

all:
	@pylint --rcfile=.pylint.rc --reports=n --score=n pyscrapers tests
	@pyflakes pyscrapers tests
	@pytest tests -qq > /dev/null
