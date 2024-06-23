# Use python 3.11 slim as base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Don't create a virtualenv
RUN poetry config virtualenvs.create false

# Copy poetry configuration files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install --no-dev

# Copy application files
COPY core/ ./core/

# Copy the elt script
COPY elt.sh /app/elt.sh

# Copy the profiles.yml file to the correct location
RUN mkdir -p /root/.dbt
COPY profiles.yml /root/.dbt/profiles.yml

# set environment variables
ENV API_KEY="none"

CMD ["/bin/bash", "/app/elt.sh"]

