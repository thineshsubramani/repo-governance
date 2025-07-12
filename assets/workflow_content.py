# This is sample workflow yaml for testing purposes
# in future releases, this will be moved to a seperate file, and the path will be configurated in config.yaml 
# for eg. workflow name, - path : /security-workflows/security-scaning.yml

def get_workflow_content():
    return """
    name: Hardening CI

    on:
      workflow_dispatch:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt

          - name: Run tests
            run: |
              echo "Running tests..."
              pytest
    """
