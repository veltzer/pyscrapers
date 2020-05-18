.PHONY: all
all:
	@pytest tests -qq > /dev/null
	@pyflakes pyscrapers tests
	@pylint --rcfile=.pylint.rc --reports=n --score=n pyscrapers tests
	@flake8 pyscrapers tests

.PHONY: pytest
pytest:
	@pytest tests

.PHONY: pyflakes
pyflakes:
	@pyflakes pyscrapers tests

.PHONY: pylint
pylint:
	@pylint --rcfile=.pylint.rc --reports=n --score=n pyscrapers tests

.PHONY: flake8
flake8:
	@flake8 pyscrapers tests

.PHONY: pyre
pyre:
	@pyre check
