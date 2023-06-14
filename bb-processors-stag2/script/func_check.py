import os

excluded_directories = ['script', 'env', 'an_example_function', 'venv', '__pycache__']

valid_directory_prefixes = ['collector_', 'processor_', 'loader_', 'utils']


def check_directory_naming():
    current_directory = os.getcwd()

    directories = []

    for item in os.listdir(current_directory):
        if os.path.isdir(item) and not item.startswith('.') and item not in excluded_directories:
            directories.append(item)

    invalid_directories = []

    for directory in directories:
        if not directory.startswith(tuple(valid_directory_prefixes)):
            invalid_directories.append(directory)

    if len(invalid_directories) > 0:
        print('\nInvalid directories:\n')
        for directory in invalid_directories:
            print(directory)
        print('\nPlease use the following prefixes:\n')
        for prefix in valid_directory_prefixes:
            print(prefix)

        exit(1)


check_directory_naming()
