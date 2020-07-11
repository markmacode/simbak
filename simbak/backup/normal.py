import logging as _logging
from simbak import fileutil as _fileutil

_logger = _logging.getLogger(__name__)


class BackupNormal():
    def __init__(self, sources: list, destinations: list, name: str,
                 compression_level: int = 6):
        """Initialize of the BackupNormal object

        Args:
            sources (list of str): Paths to the files that you are backing up.
            destinations (list of str): Paths of where you want the backup to
                be stored.
            name (str): Name of the backup, this will name the backup files.
            compression_level (int, optional): The gzip compression level that
                you want to use for the backup. Defaults to 6.
        """
        self._sources = sources
        self._destinations = destinations
        self._name = name
        self._compression_level = compression_level

    def backup(self):
        """Standard simbak backup.

        This will backup all the files defined in the sources and store them
        in a gzip'd file in each of the destinations. The name of the gzip file
        will be the name parameter suffixed with a time stamp, the format of
        the timestamp is YYYY-MM-DD--hh-mm-ss
        """
        _logger.info(f'Starting backup [{self._name}]')
        filtered_sources = _fileutil.filter_paths(self._sources)
        filtered_destinations = _fileutil.filter_paths(
            self._destinations, create=True)
        file_name = _fileutil.unique_file_name(self._name)
        _logger.info(f'Backup file name will be {self._name}')

        first_path = _fileutil.create_targz(
            sources=filtered_sources,
            destination=filtered_destinations[0],
            file_name=file_name,
            compression_level=self._compression_level
        )
        _fileutil.distribute_file(
            path=first_path,
            destinations=filtered_destinations[1:]
        )
