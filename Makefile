PYTEST := uv run pytest
PYTEST_OPTIONS := -v -s -l

.PHONY: all-tests smoke negative allure

all-tests:
	$(PYTEST) $(PYTEST_OPTIONS)

smoke:
	$(PYTEST) $(PYTEST_OPTIONS) -m smoke

negative:
	$(PYTEST) $(PYTEST_OPTIONS) -m negative

allure:
	allure serve allure-results
