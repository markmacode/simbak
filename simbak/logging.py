import logging
import logging.handlers as _handlers
import os as _os


def _set_root_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(_stream_handler())
    root_logger.addHandler(_rotating_file_handler())
    return root_logger


def _stream_handler():
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    return handler


def _rotating_file_handler():
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d, %H-%M-%S')
    handler = _handlers.RotatingFileHandler(
        _os.path.join(log_path, 'simbak.log'),
        maxBytes=1000000,
        backupCount=20)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    return handler


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

_set_root_logger()
