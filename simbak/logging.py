import logging
import logging.handlers as _handlers
import os as _os

from simbak import config as _config


def set_root_logger():
    stream_handler = _stream_handler()
    rotating_file_handler = _rotating_file_handler(get_log_path())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(rotating_file_handler)
    return root_logger


def get_log_path() -> str:
    log_path = './logs'

    if _config.SIMBAK_ENV != 'debug':
        # Windows
        if _os.name == 'nt':
            appdata = _os.getenv('APPDATA', default='C:\\Program Data')
            log_path = _os.path.join(appdata, 'simbak')
        # Linux
        elif _os.name == 'posix':
            log_path = _os.path.join('var', 'log', 'simbak')

    if _os.path.exists(log_path) is False:
        _os.mkdir(log_path)

    return log_path


def _stream_handler():
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler = logging.StreamHandler()

    if _config.SIMBAK_ENV == 'debug':
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)

    handler.setFormatter(formatter)
    return handler


def _rotating_file_handler(log_path: str):
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
