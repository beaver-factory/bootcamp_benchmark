import os

excluded_directories = ['script', 'env', 'an_example_function', 'venv', '__pycache__']

def check_directory_naming():
    current_directory = os.getcwd()

    func_app_folder = current_directory.split('/')[-1]
    if func_app_folder[-1] == 's':
        valid_directory_prefix = func_app_folder[:-1] + '_'
    else:
        valid_directory_prefix = func_app_folder + '_'

    directories = []

    for item in os.listdir(current_directory):
        if os.path.isdir(item) and not item.startswith('.') and item not in excluded_directories:
            directories.append(item)

    invalid_directories = []

    for directory in directories:
        if not directory.startswith(valid_directory_prefix):
            invalid_directories.append(directory)

    if len(invalid_directories) > 0:
        print('\nInvalid directories:\n')
        for directory in invalid_directories:
            print(directory)
        print(f'\nPlease use the following prefix for directories within this location: "{valid_directory_prefix}"')

        exit(1)


check_directory_naming()
