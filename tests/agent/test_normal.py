import os
from unittest.mock import patch
from simbak.agent import NormalAgent
from simbak.exception import BackupError
import pytest


sources = [
    os.path.join('first', 'source', 'file.txt'),
    os.path.join('second', 'source', 'other.txt'),
    os.path.join('third', 'source', 'another.txt'),
]
destinations = [
    os.path.join('first', 'destination'),
    os.path.join('second', 'destination'),
    os.path.join('third', 'destination'),
]
filtered_sources = [
    os.path.join('first', 'source', 'file.txt'),
    os.path.join('third', 'source', 'another.txt'),
]
filtered_destinations = [
    os.path.join('first', 'destination'),
    os.path.join('second', 'destination'),
    os.path.join('third', 'destination'),
]
name = 'hello'


@patch('simbak.fileutil.filter_paths')
@patch('simbak.fileutil.unique_file_name')
@patch('simbak.fileutil.create_targz')
@patch('simbak.fileutil.distribute_file')
def test__backup(mock_distribute_file, mock_create_targz,
                 mock_unique_file_name, mock_filter_paths):
    mock_filter_paths.side_effect = [filtered_sources, filtered_destinations]
    mock_unique_file_name.return_value = 'hello--1.tar.gz'
    mock_create_targz.return_value = \
        os.path.join('first', 'destination', 'hello--1.tar.gz')

    agent = NormalAgent(sources, destinations, name)
    agent.backup()

    mock_create_targz.assert_called_with(
        sources=filtered_sources,
        destination=filtered_destinations[0],
        file_name='hello--1.tar.gz',
        compression_level=6
    )
    mock_distribute_file.assert_called_with(
        path=os.path.join('first', 'destination', 'hello--1.tar.gz'),
        destinations=filtered_destinations[1:],
    )


@patch('simbak.fileutil.filter_paths')
def test__backup__no_sources(mock_filter_paths):
    mock_filter_paths.side_effect = [[], filtered_destinations]

    with pytest.raises(BackupError) as e:
        agent = NormalAgent(sources, destinations, name)
        agent.backup()

    assert str(e.value) == 'No sources for backup with NormalAgent'


@patch('simbak.fileutil.filter_paths')
def test__backup__no_destinations(mock_filter_paths):
    mock_filter_paths.side_effect = [filtered_sources, []]

    with pytest.raises(BackupError) as e:
        agent = NormalAgent(sources, destinations, name)
        agent.backup()

    assert str(e.value) == 'No destinations for backup with NormalAgent'
