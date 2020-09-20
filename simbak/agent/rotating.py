import logging as _logging
import os as _os

from simbak import fileutil as _fileutil
from simbak.agent.base import BaseAgent as _BaseAgent

_logger = _logging.getLogger(__name__)


class RotatingAgent(_BaseAgent):
    def __init__(self, sources: list, destinations: list, name: str,
                 rotate_limit: int, compression_level: int = 6):
        """
        Args:
            sources (list of str): Paths to the files that you are
                backing up.
            destinations (list of str): Paths of where you want the
                backup to be stored.
            name (str): Name of the backup, this will name the backup
                files.
            rotate_limit (int): The maximum amount of backups to keep in
                a destination.
            compression_level (int, optional): The gzip compression
                level that you want to use for the backup. Default to 6.
        """
        super().__init__(sources, destinations, name, compression_level)
        self._rotate_limit = rotate_limit

    def backup(self):
        """Rotating simbak backup.

        This will backup all the files defined in the sources and store
        them in a gzip'd file in each of the destinations. The name of
        the gzip file will be the `_name` property suffixed with a time
        stamp, the format of the timestamp is YYYY-MM-DD--hh-mm-ss

        The amount of backups in the destination will be limited by the
        `_rotate_limit` value, the oldest backup will be removed if the
        limit is exceeded.
        """
        _logger.info(f'Starting rotating backup [{self._name}]')
        _logger.info(f'Rotating limit is {self._rotate_limit}')
        super()._backup()

        for destination in self._destinations:
            # Get the valid files for this rotating agent.
            all_files = _os.listdir(destination)
            targz_files = [f for f in all_files if f.endswith('.tar.gz')]
            valid_files = [f for f in targz_files if f.startswith(self._name)]

            # Remove the oldest file(s) if the limit is surpassed.
            if len(valid_files) > self._rotate_limit:
                _logger.info(
                    f'Rotate limit has been exceeded for [{self._name}] in '
                    f'{destination}')
                oldest_file = _fileutil.oldest_file(valid_files)
                _logger.info(f'Removing oldest backup {oldest_file}')
                _os.remove(oldest_file)
