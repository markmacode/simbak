import os as _os
import tarfile as _tarfile
import logging as _logging
from datetime import datetime as _datetime
from shutil import copyfile as _copyfile

_logging.basicConfig(format='%(levelname)s: %(message)s', level=_logging.DEBUG)


def _filter_paths(paths: list, create=False) -> list:
    """
    Returned a list of paths that exist and cleans the path names. 
    Creates non-existing paths if the create param is True.
    """
    filtered_paths = []

    for path in paths:
        normpath = _os.path.normpath(path)

        if _os.path.exists(normpath):
            filtered_paths.append(normpath)
        elif create == True:
            _logging.info(
                f'{normpath} doesn\'t exist, creating directory with that path.')
            _os.makedirs(normpath)
            filtered_paths.append(normpath)

    return filtered_paths


def _unique_file_name(file_name: str) -> str:
    """Creates a unique file name by suffixing date and time"""
    time_suffix = _datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    file_name = f'{file_name}--{time_suffix}.tar.gz'
    return file_name


def _create_backup(sources: list, destination: str, name: str, compression_level: int):
    """Creates the backup file in the first destination"""
    first_path = _os.path.join(destination, name)

    try:
        tar = _tarfile.open(first_path, 'x:gz', compresslevel=compression_level)

        for source in sources:
            basename = _os.path.basename(source)
            _logging.info(f'Compressing {source}')
            try:
                tar.add(source, basename)
            except PermissionError:
                _logging.error(
                    f'Couldn\'t compress {source}, pemission denied.')

        tar.close()
        _logging.info(f'Saved backup {name} to {destination}')
    except FileExistsError:
        _logging.error(f'Failed to create backup {name}, file already exists')

    return first_path


def _distribute_backup(backup_path: str, destinations: list, name: str):
    """Copy backup file to each of the destinations"""
    for destination in destinations:
        path = _os.path.join(destination, name)
        _copyfile(backup_path, path)
        _logging.info(f'Saved backup {name} to {destination}')


def backup(sources: list, destinations: list, name: str, compression_level: int = 6):
    sources = _filter_paths(sources)
    destinations = _filter_paths(destinations, create=True)
    name = _unique_file_name(name)

    first_path = _create_backup(sources, destinations[0], name,
                                compression_level)
    _distribute_backup(first_path, destinations[1:], name)
