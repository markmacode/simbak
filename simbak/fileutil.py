import logging as _logging
import os as _os
import shutil as _shutil
import tarfile as _tarfile
from datetime import datetime as _datetime

_logger = _logging.getLogger(__name__)


def filter_paths(paths: list, create=False) -> list:
    """Gets only existing paths and cleans the paths to be OS compliant.

    Args:
        paths (list of str): The list of paths that needs to be
            filtered.
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
        to_path = _os.path.join(destination, file_name)
        _shutil.copyfile(path, to_path)
        _logger.info(f'Saved backup {file_name} to {destination}')


def create_targz(sources: list, destination: str, file_name: str,
                 compression_level: int = 6) -> str:
    """Creates a tar.gz file in a single destination.

    If you try to create a tar.gz file for a file that already exists,
    it will not overwrite that file.

    Args:
        sources (list of str): The paths of the files you want to file.
        destination (str): The path of where you want the file to be
            stored.
        file_name (str): The name that the file will be.
        compression_level (int): The gzip compression level that you
            want to use for the file.

    Returns:
        str: Path of the file that was created, if the file already
            existed, it will return the already existing file path.
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


def dir_size(base_path: str = '.') -> int:
    """Gets the total size of a directory, in bytes.

    Args:
        base_path (str, optional): Path to the dir to get the size of.

    Returns:
        int: Size of the directory, in bytes.
    """
    size = 0

    for dir_path, dir_names, file_names in _os.walk(base_path):
        for file_name in file_names:
            file_path = _os.path.join(dir_path, file_name)

            # Skip if it is symbolic link.
            if not _os.path.islink(file_path):
                size += _os.path.getsize(file_path)

    return size
