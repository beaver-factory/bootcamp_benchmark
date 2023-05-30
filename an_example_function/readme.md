# Example function

## Set up a function

To set up a new function, run:

```
    make func dir=function_name
```

Make sure you follow this naming convention:

| Focus                  | Name                      |
| ---------------------- | ------------------------- |
| Collecting from source | `collector_function_name` |
| Processing data        | `processor_function_name` |
| Loading data into db   | `loader_function_name`    |

<br></br>
Then, follow the terminal instructions to set up your azure function as required by selecting a trigger type. This will create a named directory with an `__init__.py`, a `function.json` and a `readme.md`. It will also copy the example `app.py` and `__tests__` directory from `an_example_function`.

## Example folder structure

```
    function_name/
    ├─ __tests__/
    │  ├─ __init__.py
    │  ├─ test_app.py
    ├─ __init__.py
    ├─ app.py
    ├─ function.json
```

## File information

- Function logic is split up into `__init__.py` and `app.py`.
  - `function_name/__init__.py` is where any azure-centric code goes, e.g interacting directly with blob storage.
  - `function_name/app.py` is where all other function logic goes.
  - For example, when dealing with blob containers, once you read from a blob, it should enter directly into `app.py`. After leaving `app.py` it should write directly to blob storage.
- `__tests__/__init__.py` should remain empty.
- `__tests__/test_app.py` should test the functionality of `app.py` as there should be minimal code in `__init__.py`.
- After creating the function directory, within `function.json` you will need to provide updated information for the azure bindings and update the name of your primary function in app.py.
