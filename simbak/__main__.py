import sys

from simbak.cli import main
from simbak.exception import BackupError
import logging as _logging


_logger = _logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BackupError as backup_error:
        _logger.error(backup_error)
        sys.exit(1)
