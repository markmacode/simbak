from deprecation import deprecated
from simbak.backup import backup as _backup
import simbak


@deprecated(deprecated_in='0.1.2', removed_in='0.2.0',
            current_version=simbak.__version__,
            details='Use simbak.backup.backup function instead.')
def backup(sources: list, destinations: list, name: str,
           compression_level: int = 6):
    _backup(sources, destinations, name, compression_level)
