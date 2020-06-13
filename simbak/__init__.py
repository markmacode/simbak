import os as _os
import logging as _logging
import logging.handlers as _handlers


__version__ = '0.1.2'

# Setting up logger
if _os.path.exists('logs/') is False:
    _os.mkdir('logs/')

_stream_formatter = _logging.Formatter('%(levelname)s: %(message)s')
rotating_file_formatter = _logging.Formatter(
    fmt='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H-%M-%S'
)

_stream_handler = _logging.StreamHandler()
_stream_handler.setLevel(_logging.INFO)
_stream_handler.setFormatter(_stream_formatter)

_rotating_file_handler = _handlers.RotatingFileHandler(
    'logs/simbak.log', maxBytes=1000000, backupCount=20)
_rotating_file_handler.setLevel(_logging.DEBUG)
_rotating_file_handler.setFormatter(rotating_file_formatter)

_root_logger = _logging.getLogger()
_root_logger.setLevel(_logging.DEBUG)
_root_logger.addHandler(_stream_handler)
_root_logger.addHandler(_rotating_file_handler)
