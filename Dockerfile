FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update \
     && apt-get install -y --no-install-recommends git curl npm \
     && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy only necessary files
COPY ./.pre-commit-config.yaml \
     ./pylintrc \
     ./pyproject.toml \
     ./requirements.txt \
     ./setup.cfg \
     ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize Git repository and set up pre-commit hooks
RUN git init . && pre-commit install-hooks

# Display versions
RUN python --version && \
    pip --version && \
    pre-commit --version
