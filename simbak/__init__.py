from simbak.logging import logging
from simbak.agent.normal import NormalAgent as _NormalAgent

__version__ = '0.2.1'
_logger = logging.getLogger(__name__)


def backup(sources: list, destinations: list, name: str,
           compression_level: int = 6):
    """The easiest way to perform a standard backup.

    Args:
        sources (list of str): Paths to the files that you are backing
            up.
        destinations (list of str): Paths of where you want the backup
            to be stored.
        name (str): Name of the backup, this will name the backup files.
        compression_level (int, optional): The gzip compression level
            that you want to use for the backup. Defaults to 6.
    """
    agent = _NormalAgent(sources, destinations, name, compression_level)
    agent.backup()
