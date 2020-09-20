import logging as _logging
import os as _os

from simbak import fileutil as _fileutil
from simbak.agent.base import BaseAgent as _BaseAgent

_logger = _logging.getLogger(__name__)


class NormalAgent(_BaseAgent):
    def __init__(self, sources: list, destinations: list, name: str,
                 compression_level: int = 6):
        super().__init__(sources, destinations, name, compression_level)

    def backup(self):
        """Standard simbak backup.

        This will backup all the files defined in the sources and store
        them in a gzip'd file in each of the destinations. The name of
        the gzip file will be the name parameter suffixed with a time
        stamp, the format of the timestamp is YYYY-MM-DD--hh-mm-ss
        """
        # Cleans the path names, and removes non-existent paths, if relevant.
        _logger.info(f'Starting backup [{self._name}]')
        _logger.info(f'{self._sources_size()} bytes for {self._name} sources')

        # A unique file name is important for certain backup agents.
        file_name = _fileutil.unique_file_name(self._name)
        _logger.info(f'Backup file name will be {file_name}')

        # Using tar gzip for the backup. Tarring once, distributing later.
        first_path = _fileutil.create_targz(
            sources=self._sources,
            destination=self._destinations[0],
            file_name=file_name,
            compression_level=self._compression_level)
        backup_size = _os.path.getsize(first_path)
        _logger.info(f'{backup_size} bytes for {self._name} backup file')

        _fileutil.distribute_file(
            path=first_path,
            destinations=self._destinations[1:])
