from unittest.mock import call
import os
from unittest.mock import patch

import pytest

from simbak.agent import RotatingAgent
from simbak.exception import BackupError

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


@patch('simbak.agent.base._fileutil')
@patch('simbak.agent.rotating._os')
@patch('simbak.agent.base._os')
def test__backup(mock_base_os, mock_os, mock_base_fileutil):
    mock_base_fileutil.filter_paths.side_effect = [
        filtered_sources, filtered_destinations
    ]
    mock_base_fileutil.unique_file_name.return_value = 'hello--1.tar.gz'
    mock_base_fileutil.create_targz.return_value = \
        os.path.join('first', 'destination', 'hello--1.tar.gz')
    mock_base_fileutil.dir_size.return_value = 10
    mock_base_os.path.getsize.return_value = 20
    mock_os.listdir.return_value = [
        'hello--0.tar.gz'
    ]

    agent = RotatingAgent(sources, destinations, name, 3)
    agent.backup()

    mock_base_fileutil.create_targz.assert_called_with(
        sources=filtered_sources,
        destination=filtered_destinations[0],
        file_name='hello--1.tar.gz',
        compression_level=6
    )
    mock_base_fileutil.distribute_file.assert_called_with(
        path=os.path.join('first', 'destination', 'hello--1.tar.gz'),
        destinations=filtered_destinations[1:],
    )


@patch('simbak.agent.rotating._fileutil')
@patch('simbak.agent.base._fileutil')
@patch('simbak.agent.rotating._os.remove')
@patch('simbak.agent.rotating._os.listdir')
@patch('simbak.agent.base._os')
def test__backup__rotate_limit_exceeded(
        mock_base_os, mock_os_listdir, mock_os_remove, mock_base_fileutil,
        mock_fileutil):
    mock_base_fileutil.filter_paths.side_effect = [
        filtered_sources, filtered_destinations
    ]
    mock_base_fileutil.unique_file_name.return_value = 'hello--4.tar.gz'
    mock_base_fileutil.create_targz.return_value = os.path.join(
        'first', 'destination', 'hello--4.tar.gz')
    mock_base_fileutil.dir_size.return_value = 10
    mock_base_os.path.getsize.return_value = 20
    mock_os_listdir.return_value = [
        'hello--1.tar.gz',
        'hello--2.tar.gz',
        'hello--3.tar.gz',
        'hello--4.tar.gz',
    ]
    mock_fileutil.oldest_file.return_value = 'hello--1.tar.gz'

    agent = RotatingAgent(sources, destinations, name, 3)
    agent.backup()

    mock_base_fileutil.create_targz.assert_called_with(
        sources=filtered_sources,
        destination=filtered_destinations[0],
        file_name='hello--4.tar.gz',
        compression_level=6
    )
    mock_base_fileutil.distribute_file.assert_called_with(
        path=os.path.join('first', 'destination', 'hello--4.tar.gz'),
        destinations=filtered_destinations[1:],
    )
    mock_os_remove.assert_has_calls([
        call(os.path.join('first', 'destination', 'hello--1.tar.gz')),
        call(os.path.join('second', 'destination', 'hello--1.tar.gz')),
        call(os.path.join('third', 'destination', 'hello--1.tar.gz')),
    ])


@patch('simbak.agent.base._fileutil')
def test__backup__no_sources(mock_base_fileutil):
    mock_base_fileutil.filter_paths.side_effect = [[], filtered_destinations]

    with pytest.raises(BackupError) as e:
        agent = RotatingAgent(sources, destinations, name, 1)
        agent.backup()

    assert str(e.value) == 'No sources for backup'


@patch('simbak.agent.base._fileutil')
def test__backup__no_destinations(mock_base_fileutil):
    mock_base_fileutil.filter_paths.side_effect = [filtered_sources, []]

    with pytest.raises(BackupError) as e:
        agent = RotatingAgent(sources, destinations, name, 1)
        agent.backup()

    assert str(e.value) == 'No destinations for backup'
