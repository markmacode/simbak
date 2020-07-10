import logging as _logging
import os as _os
import tarfile as _tarfile
from datetime import datetime as _datetime
from shutil import copyfile as _copyfile

_logger = _logging.getLogger(__name__)


def filter_paths(paths: list, create=False) -> list:
    """Gets only existing paths and cleans the paths to be OS compliant.

    Args:
        paths (list of str): The list of paths that needs to be filtered.
        create (bool, optional): Create a path if it doesn't exist.
            Defaults to False.

    Returns:
        list of str: The filtered list of paths.
    """
    filtered_paths = []

    for path in paths:
        normpath = _os.path.normpath(path)

        if _os.path.exists(normpath):
            filtered_paths.append(normpath)
        elif create:
            _logger.info(f'{normpath} doesn\'t exist, creating directory '
                         'with that path.')
            _os.makedirs(normpath)
            filtered_paths.append(normpath)
        else:
            _logger.warning(
                f'Failed to access {normpath}, it doesn\'t exist')

    return filtered_paths


def unique_file_name(name: str) -> str:
    """Creates a unique file name by suffixing date and time.

    Args:
        name (str): The prefix of the unique file name.

    Returns:
        str: The unique file in the format of
            <name>--YYYY-MM-DD--hh-mm-ss.tar.gz
    """
    time_suffix = _datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    file_name = f'{name}--{time_suffix}.tar.gz'
    return file_name


def distribute_file(path: str, destinations: list):
    """Distributes a backup file to other destinations.

    Args:
        path (str): Path to the file that you want to distribute.
        destinations (list of str): Paths of where you want the file to
            be stored.
    """
    file_name = _os.path.basename(path)

    for destination in destinations:
        path = _os.path.join(destination, file_name)
        _copyfile(path, path)
        _logger.info(f'Saved backup {file_name} to {destination}')


def create_targz(sources: list, destination: str, file_name: str,
                 compression_level: int) -> str:
    """Creates a backup in a single destination.

    Args:
        sources (list of str): The paths of the files you want to backup.
        destination (str): The path of where you want the backup to be
            stored.
        file_name (str): The name that the backup file will be.
        compression_level (int): The gzip compression level that you want
            to use for the backup.

    Returns:
        str: Path of the backup that was created.
    """
    path = _os.path.join(destination, file_name)

    try:
        tar = _tarfile.open(path, 'x:gz',
                            compresslevel=compression_level)

        for source in sources:
            basename = _os.path.basename(source)
            _logger.info(f'Compressing {source}')
            try:
                tar.add(source, basename)
            except PermissionError:
                _logger.error(f'Couldn\'t compress {source}, pemission '
                              'denied.')

        tar.close()
        _logger.info(f'Saved backup {file_name} to {destination}')
    except FileExistsError:
        _logger.error(f'Failed to create backup {file_name}, file already '
                      'exists')

    return path
