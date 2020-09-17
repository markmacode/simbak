import logging
import logging.handlers as _handlers
import os as _os

# Setting up logger files
log_path = './simbak.log'

# Windows
if _os.name == 'nt':
    appdata = _os.getenv('APPDATA', default='C:\\Program Data')
    log_path = _os.path.join(appdata, 'simbak')
# Linux
elif _os.name == 'posix':
    log_path = _os.path.join('var', 'log', 'simbak')

if _os.path.exists(log_path) is False:
    _os.mkdir(log_path)

# Setting up the format of the logs.
_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
rotating_file_formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d, %H-%M-%S'
)

# Stream handler for logging to the terminal.
_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.INFO)
_stream_handler.setFormatter(_stream_formatter)

# File handler for logging to a file.
_rotating_file_handler = _handlers.RotatingFileHandler(
    _os.path.join(log_path, 'simbak.log'), maxBytes=1000000, backupCount=20)
_rotating_file_handler.setLevel(logging.DEBUG)
_rotating_file_handler.setFormatter(rotating_file_formatter)

_root_logger = logging.getLogger()
_root_logger.setLevel(logging.DEBUG)
_root_logger.addHandler(_stream_handler)
_root_logger.addHandler(_rotating_file_handler)
