# Bootcamp Benchmark

This project contains Azure functions that, when deployed together, form a data pipeline for a digital skills provider analytics dashboard. 

We hope to be able to answer the following question with this analytics dashboard:

1. How do digital skills providers and their respective courses meet current job market demand?

The current setup deploys these functions between three function apps so ensure you have followed the appropriate setup in the [infra repo](https://github.com/northcoders-dev/bootcamp_benchmark_infra). 

## Requirements

Before getting started, make sure you have [`Python 3`](https://www.python.org/downloads/) installed along with `pip3`. 

## Setup

Since each function app can be deployed independently, each contains its own `Makefile` for useful commands and a `requirements.txt` file for setting up a virtual environment. The root directory also contains a `Makefile` and `requirements.txt` for repo wide commands. 

After cloning the repo, you can set up each virtual environment and install the appropriate dependencies with `pip3` in one go by running the following command from the root directory:

```bash
make setup_repo
```

Alternatively, you can do this for a single function app by navigating into the appropriate directory and running:

```bash
make setup
```

## Linting

This project uses `flake8` for code linting. Navigate to the root directory to lint across the whole repo, or into a specific function app directory to lint only files within that project. Then run:

```bash
make lint
```

This command will run `flake8` on all the python files in the project.

## Testing

This project uses `pytest` for testing. To run the tests for a function app, navigate to the appropriate directory and use:

```bash
make unit_test
```

This command will run all the unit tests in the project and provide a verbose output.

For tests in the `loader` function app, you will need to run tests against a containerised PostgreSQL server. You will first need to have `Docker` running and then run 
```bash
make dock
```

## Adding Dependencies

To install a package into a virtual environment and add to the `requirements.txt`, run

```bash
make dependency
```

from either the root directory or a specific function app directory.

## Prune Dependencies

To check for surplus dependencies in your `requirements.txt` file, navigate to the function app directory and run

```bash
make prune
```

## Creating a Function

To add a new function to a function app, follow the steps found in [an_example_function](an_example_function/readme.md) from within the directory.

## Check Function Conformity

To check your directories follow the correct naming structure, navigate into a function app directory and run 

```bash
make func_check
```

## Adding Secrets

Before deploying the `collectors` function app, check if the repo has secrets set for `ADZUNA_APP_KEY` and `ADZUNA_APP_ID` by running 
``` bash
gh secret list
```

If these values are not set in the repo secrets, create their values from the Adzuna API and add them to a root level `.env`.

Then `cd collectors` and run 
``` bash
make adzuna_secrets
``` 

to set these values as GitHub secrets which are then read during the collectors deployment and added to the Azure Key Vault.

## Deployment

As with the [infra repo](https://github.com/northcoders-dev/bootcamp_benchmark_infra), this project contains workflows that allow deployment to either a staging or production environment.

For the staging environment, each function app can be deployed independently. The current triggers are changes on `main` to either the function app directory or its workflow file.

To change which resource group or function app your directory will deploy to, update the environment variables in the appropriate workflow file, for example:

```
env:
  FUNCTION_APP_NAME: bb-processors-stag2
  RESOURCE_GROUP_NAME: alexBootcampBenchmarkStaging
  AZURE_FUNCTIONAPP_PACKAGE_PATH: './processors' 
  AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS_2 }}
```

The `FUNCTION_APP_NAME` and `RESOURCE_GROUP_NAME` should match the values defined in the infra repo. `AZURE_FUNCTIONAPP_PACKAGE_PATH` should match the path to the directory you wish to deploy. As described in the [infra repo](https://github.com/northcoders-dev/bootcamp_benchmark_infra), you should ensure the GitHub secrets for this repo contain your Azure credentials. 

<!-- TODO: add details of production deployment once we've figured it out! -->

## Versioning and Creating New Tags

This project uses Semantic Versioning [SemVer](https://semver.org/) to manage version numbers and changes. There are three types of version changes:

- Major (v=major): These are breaking changes that aren't backward-compatible with older versions. For example, this would be appropriate for a major overhaul of the codebase or functionality.

- Minor (v=minor): These are backward-compatible changes that add new functionality or features to the project without disturbing the existing API.

- Patch (v=patch): These are backward-compatible bug fixes intended to correct any wrong behavior.

To create a new tag, use the following command at root level:

```bash
make tag v=[type]
```

Replace [type] with major, minor, or patch depending on the nature of the changes you've made. This will create and publish a new SemVer tag for your current state of the project.
