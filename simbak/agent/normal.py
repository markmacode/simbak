import logging as _logging

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
        sources, destinations = super()._filter_paths(
            self._sources, self._destinations)

        # A unique file name is important for certain backup agents.
        file_name = _fileutil.unique_file_name(self._name)
        _logger.info(f'Backup file name will be {file_name}')

        # Using tar gzip for the backup. Tarring once, distributing later.
        first_path = _fileutil.create_targz(
            sources=sources,
            destination=destinations[0],
            file_name=file_name,
            compression_level=self._compression_level)

        super()._log_source_sizes(sources)
        super()._log_backup_size(first_path)

        _fileutil.distribute_file(
            path=first_path,
            destinations=destinations[1:])
