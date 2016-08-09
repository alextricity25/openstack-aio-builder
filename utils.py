# Random methods that come in handy throughout the project

import yaml
import os

def get_meta_file(file_path):
    """
    Takes in a yaml file, and returns it's corresponding python dictionary

    :param file_path: String of the absolute or relative file path of the file.
    :return: dict()
    """
    # Read the yaml file and return a dictionary
    with open(file_path, 'r') as f:
        file_dict = yaml.safe_load(f)

    return file_dict