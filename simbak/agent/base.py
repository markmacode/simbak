import abc as _abc
import logging as _logging
import os as _os

from simbak.exception import BackupError as _BackupError
from simbak.fileutil import dir_size as _dir_size

_logger = _logging.getLogger(__name__)


class BaseAgent(_abc.ABC):
    def __init__(self, sources: list, destinations: list, name: str,
                 compression_level: int):
        """Initializer of the NormalAgent object

        Args:
            sources (list of str): Paths to the files that you are
                backing up.
            destinations (list of str): Paths of where you want the
                backup to be stored.
            name (str): Name of the backup, this will name the backup
                files.
            compression_level (int, optional): The gzip compression
                level that you want to use for the backup. Defaults to 6.
        """
        self._sources = sources
        self._destinations = destinations
        self._name = name
        self._compression_level = compression_level

    @staticmethod
    def _log_source_sizes(sources: list):
        for source in sources:
            size = _dir_size(source)
            _logger.info(f'{size} bytes :: SOURCE :: {source}')

    @staticmethod
    def _log_backup_size(backup_path: str):
        size = _os.path.getsize(backup_path)
        _logger.info(f'{size} bytes :: BACKUP :: {backup_path}')

    @staticmethod
    def _validate_paths(sources: list, destinations: list):
        if len(sources) == 0:
            raise _BackupError('No sources for backup')
        if len(destinations) == 0:
            raise _BackupError('No destinations for backup')
