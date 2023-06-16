# Bootcamp Benchmark

This project contains azure functions that, when deployed together, form a data pipeline for a digital skills provider analytics dashboard.

We hope to be able to answer the following questions with this analytics dashboard:

1. (first q here)

We use a Makefile to simplify some common tasks.

## Requirements

Before getting started, make sure you have [Python 3](https://www.python.org/downloads/) installed along with pip3.

## Setup

After cloning the project, you should install the required dependencies. You can do this with the following command:

```bash
make setup
```

This command will use pip3 to install the dependencies listed in the `requirements.txt` file.

## Adding dependencies

```bash
make dependency
```

## Linting

This project uses flake8 for code linting. To run the linter, use:

```bash
make lint
```

This command will run flake8 on all the python files in the project.

## Running Tests

This project uses pytest for testing. To run the tests, use:

```bash
make unit_test
```

This command will run all the unit tests in the project and provide a verbose output.

In order to run tests against a containerised PostgreSQL server, you will first need to have docker running and then run 
```
make dock
```

## Versioning and Creating New Tags

This project uses Semantic Versioning (SemVer)[https://semver.org/] to manage version numbers and changes. There are three types of version changes:

- Major (v=major): These are breaking changes that aren't backward-compatible with older versions. For example, this would be appropriate for a major overhaul of the codebase or functionality.

- Minor (v=minor): These are backward-compatible changes that add new functionality or features to the project without disturbing the existing API.

  -Patch (v=patch): These are backward-compatible bug fixes intended to correct any wrong behavior.

To create a new tag, use the command:

```bash
make tag v=[type]
```

Replace [type] with major, minor, or patch depending on the nature of the changes you've made. This will create and publish a new SemVer tag for your current state of the project.

## Adding a function

To add a new function to the project, please refer to [an_example_function](an_example_function/readme.md).

## Adding secrets

Before deploying the `collectors` function app, check if the repo has secrets set for `ADZUNA_APP_KEY` and `ADZUNA_APP_ID` by running `gh secret list`.

If these values are not set in the repo secrets, create their values from the Adzuna API and add them to a root level .env

Then `cd collectors` and run `make adzuna_secrets` to set these values as GitHub secrets which are then read during the collectors deployment and added to the Azure Key Vault.