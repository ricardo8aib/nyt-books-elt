# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
SHELL = /bin/bash
OS = $(shell uname | tr A-Z a-z)

# Define environment variables
START_DATE := 2021-01-01
END_DATE := 2024-01-10
API_KEY := "API_KEY"

.PHONY: check-pre-commit
check-pre-commit: ## Checks pre-commit hooks
	pre-commit run --all-files

.PHONY: ingest
ingest:  ## Run the data load tool script
	@export START_DATE=$(START_DATE) && \
	export END_DATE=$(END_DATE) && \
	export API_KEY=$(API_KEY) && \
	poetry run python core/data_retrieval/ingestion.py

.PHONY: model
model:  ## Run the dbt script
	(cd core/dimensional_modeling; poetry run dbt run)

.PHONY: run-queries
run-queries:  ## Run the queries
	poetry run python core/sql_queries/query_executor.py