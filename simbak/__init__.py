from dotenv import load_dotenv as _load_dotenv

__version__ = '0.3.1'


def main():
    from simbak.logging import set_root_logger
    set_root_logger()


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
    from simbak.agent.normal import NormalAgent
    agent = NormalAgent(sources, destinations, name, compression_level)
    agent.backup()


_load_dotenv()
main()
