import abc as _abc
import logging as _logging

from simbak import fileutil as _fileutil
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

        self.__filter_paths()

    def __filter_paths(self, create: bool = True):
        self._sources = _fileutil.filter_paths(self._sources)
        self._destinations = _fileutil.filter_paths(
            self._destinations, create=create)
        self._validate_paths()

    def _validate_paths(self):
        if len(self._sources) == 0:
            raise _BackupError('No sources for backup')
        if len(self._destinations) == 0:
            raise _BackupError('No destinations for backup')

    def _sources_size(self):
        total_size = 0
        for source in self._sources:
            dir_size = _dir_size(source)
            total_size += dir_size

        return total_size
