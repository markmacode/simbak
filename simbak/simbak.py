import os
import tarfile
import logging
from datetime import datetime
from shutil import copyfile

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def _filter_paths(paths: list, create=False) -> list:
    """
    Returned a list of paths that exist and cleans the path names. 
    Creates non-existing paths if the create param is True.
    """
    filtered_paths = []

    for path in paths:
        normpath = os.path.normpath(path)

        if os.path.exists(normpath):
            filtered_paths.append(normpath)
        elif create == True:
            logging.info(
                f'{normpath} doesn\'t exist, creating directory with that path.')
            os.makedirs(normpath)
            filtered_paths.append(normpath)

    return filtered_paths


def _unique_file_name(file_name: str) -> str:
    """Creates a unique file name by suffixing date and time"""
    time_suffix = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    file_name = f'{file_name}--{time_suffix}.tar.gz'
    return file_name


def _create_backup(sources: list, destination: str, name: str, compression_level: int):
    """Creates the backup file in the first destination"""
    first_path = os.path.join(destination, name)

    try:
        tar = tarfile.open(first_path, 'x:gz', compresslevel=compression_level)

        for source in sources:
            basename = os.path.basename(source)
            logging.info(f'Compressing {source}')
            try:
                tar.add(source, basename)
            except PermissionError:
                logging.error(
                    f'Couldn\'t compress {source}, pemission denied.')

        tar.close()
        logging.info(f'Saved backup {name} to {destination}')
    except FileExistsError:
        logging.error(f'Failed to create backup {name}, file already exists')

    return first_path


def _distribute_backup(backup_path: str, destinations: list, name: str):
    """Copy backup file to each of the destinations"""
    for destination in destinations:
        path = os.path.join(destination, name)
        copyfile(backup_path, path)
        logging.info(f'Saved backup {name} to {destination}')


def backup(sources: list, destinations: list, name: str, compression_level: int = 6):
    sources = _filter_paths(sources)
    destinations = _filter_paths(destinations, create=True)
    name = _unique_file_name(name)

    first_path = _create_backup(sources, destinations[0], name,
                                compression_level)
    _distribute_backup(first_path, destinations[1:], name)
