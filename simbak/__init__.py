from dotenv import load_dotenv as _load_dotenv
from simbak.logging import set_logger as _set_logger

__version__ = '0.4.1'

_load_dotenv()
_set_logger()


def backup(sources: list, destinations: list, name: str,
           compression_level: int = 6, log_path: str = None):
    """The easiest way to perform a standard backup.

    Args:
        sources (list of str): Paths to the files that you are backing
            up.
        destinations (list of str): Paths of where you want the backup
            to be stored.
        name (str): Name of the backup, this will name the backup files.
        compression_level (int, optional): The gzip compression level
            that you want to use for the backup. Defaults to 6.
        log_path (str, optional): The file location to store the logs.
    """
    from simbak.agent.normal import NormalAgent
    from simbak.logging import set_file_logger

    if log_path is not None:
        set_file_logger(log_path)

    agent = NormalAgent(sources, destinations, name, compression_level)
    agent.backup()
