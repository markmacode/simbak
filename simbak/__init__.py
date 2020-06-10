import os as _os
import logging as _logging
import logging.handlers as _handlers

if _os.path.exists('logs/') == False:
    _os.mkdir('logs/')

# Setting up logger
stream_formatter = _logging.Formatter('%(levelname)s: %(message)s')
rotating_file_formatter = _logging.Formatter(
    fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H-%M-%S')

stream_handler = _logging.StreamHandler()
stream_handler.setLevel(_logging.INFO)
stream_handler.setFormatter(stream_formatter)

rotating_file_handler = _handlers.RotatingFileHandler(
    'logs/simbak.log', maxBytes=1000000, backupCount=20)
rotating_file_handler.setLevel(_logging.DEBUG)
rotating_file_handler.setFormatter(rotating_file_formatter)

root_logger = _logging.getLogger()
root_logger.setLevel(_logging.DEBUG)
root_logger.addHandler(stream_handler)
root_logger.addHandler(rotating_file_handler)
