import simbak
import pytest


@pytest.fixture
def sources(tmp_path):
    file_content = 'hello world'
    sources = [
        tmp_path / 'dir',
        tmp_path / 'file.txt',
    ]
    sources[0].mkdir()
    sources[1].write_text(file_content)
    return sources


@pytest.fixture
def destinations(tmp_path):
    return [
        tmp_path / 'dest1',
        tmp_path / 'dest2',
    ]


@pytest.fixture
def log_path(tmp_path):
    return tmp_path / 'logs'


def test__backup(sources, destinations, log_path):
    simbak.backup(sources, destinations, 'test')
    assert len(list(destinations[0].iterdir())) == 1
    assert len(list(destinations[1].iterdir())) == 1
    assert log_path.exists() is False


def test__backup__with_file_logging(sources, destinations, log_path):
    simbak.backup(sources, destinations, 'test', log_path=log_path)
    assert len(list(destinations[0].iterdir())) == 1
    assert len(list(destinations[1].iterdir())) == 1
    assert log_path.exists() is True
