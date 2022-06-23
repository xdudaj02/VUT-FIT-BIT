"""
This file offers utility function used in the process of generating maps.

file:   map_util.py
author: Jakub Duda, xdudaj02
date:   8. 5. 2022
"""

import uuid
import os
from pathlib import Path


class Layer:
    """Class used to represent a layer of the map.

    Attributes:
        name        Name of this layer
        order       Order in which this layer is added to map
        style       Name of style rule that is to be used for this later
        query       Database query used to get data for this layer
    """
    def __init__(self, name, order, style_name, query):
        self.name = name
        self.order = order
        self.style = style_name
        self.query = query


def save_file(path, file, extension):
    """Saves given File object with given path prefix and given extension. Creates path if does not exist. Uses uuid
    to create a random string to use as filename. Tries with a new filename in case of collision. Runs until successful.

    :param path: Path prefix to use.
    :param file: File object to save.
    :param extension: File extension to use.
    :return: Name of new successfully created file.
    """
    while True:
        Path(path).mkdir(parents=True, exist_ok=True)
        try:
            filename = path + '/' + uuid.uuid4().hex + '.' + extension
            file.save(filename)
            return filename
        except OSError:
            pass


def save_raster_file(image, file_type, path=''):
    """Saves given Image object with given path prefix and given extension.  Creates path if does not exist. Uses uuid
    to create a random string to use as filename. Tries with a new filename in case of collision. Runs until successful.

    :param image: Image object to save as file
    :param file_type: File type - as supported by Image.
    :param path: Path prefix to use, defaults to empty string.
    :return: Name of new successfully created file.
    """
    type_string = 'jpeg100' if file_type == 'jpg' else file_type
    Path(path).mkdir(parents=True, exist_ok=True)
    while True:
        try:
            filename = path + '/' + uuid.uuid4().hex + '.' + file_type
            image.save(filename, type_string)
            return filename
        except OSError:
            pass


def generate_vector_filename(extension, path=''):
    """Generates a new filename.  Creates path if does not exist. Uses uuid to create a random string to use as
    filename. Tries with a new filename in case of collision. Runs until successful.

    :param extension: Extension of new file.
    :param path: Path prefix to use, defaults to empty string.
    :return: New filename which is available.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    while True:
        filename = path + '/' + uuid.uuid4().hex + '.' + extension
        if not os.path.exists(filename):
            return filename

