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
make install
```

This command will use pip3 to install the dependencies listed in the `requirements.txt` file.

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
