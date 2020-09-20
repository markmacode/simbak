import logging as _logging

from simbak.agent.base import BaseAgent as _BaseAgent

_logger = _logging.getLogger(__name__)


class NormalAgent(_BaseAgent):
    def __init__(self, sources: list, destinations: list, name: str,
                 compression_level: int = 6):
        """
        Args:
            sources (list of str): Paths to the files that you are
                backing up.
            destinations (list of str): Paths of where you want the
                backup to be stored.
            name (str): Name of the backup, this will name the backup
                files.
            compression_level (int, optional): The gzip compression
                level that you want to use for the backup. Default to 6.
        """
        super().__init__(sources, destinations, name, compression_level)

    def backup(self):
        """Standard simbak backup.

        This will backup all the files defined in the sources and store
        them in a gzip'd file in each of the destinations. The name of
        the gzip file will be the name parameter suffixed with a time
        stamp, the format of the timestamp is YYYY-MM-DD--hh-mm-ss
        """
        _logger.info(f'Starting backup [{self._name}]')
        super()._backup()
