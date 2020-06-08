import os as _os
import logging as _logging
from datetime import datetime as _datetime


def _get_log_file_path():
    time_suffix = _datetime.now().strftime('%Y-%m-%d--%H-%M-%S-%f')
    normpath = _os.path.normpath(f'/simbak_logs/simbak--{time_suffix}.txt')

    if _os.path.exists('/simbak_logs/') == False:
        _os.makedirs('/simbak_logs/')

    return normpath


def _get_logger():
    stream_formatter = _logging.Formatter('%(levelname)s: %(message)s')
    stream_handler = _logging.StreamHandler()
    stream_handler.setLevel(_logging.INFO)
    stream_handler.setFormatter(stream_formatter)

    file_formatter = _logging.Formatter(
        fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H-%M-%S')
    file_handler = _logging.FileHandler(_get_log_file_path())
    file_handler.setLevel(_logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    logger = _logging.getLogger(__name__)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
