# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
SHELL = /bin/bash
OS = $(shell uname | tr A-Z a-z)

.PHONY: check-pre-commit
check-pre-commit: ## Checks pre-commit hooks
	pre-commit run --all-files