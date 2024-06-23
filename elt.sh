#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Check if the environment variables START_DATE and END_DATE are set
if [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
  echo "START_DATE and END_DATE environment variables must be set."
  exit 1
fi

# Define functions to run each command
function ingest() {
    echo "Running data ingestion between $START_DATE and $END_DATE..."
    poetry run python core/data_retrieval/ingestion.py
}

function model() {
    echo "Running dbt..."
    (cd core/dimensional_modeling && poetry run dbt run)
}

function run_queries() {
    echo "Running SQL queries..."
    poetry run python core/sql_queries/query_executor.py
}

function copy_database() {
    echo "Copying nyt_books.duckdb to output_db directory..."
    mkdir -p output_db  # Create output_db directory if it doesn't exist
    cp nyt_books.duckdb output_db/nyt_books.duckdb
}

# Run each function
ingest
model
run_queries

# Copy the database file
copy_database

echo "All commands executed successfully!"
echo "You can check the query results here: core/sql_queries/"
echo "You can check the duckdb database here: output_db/"
