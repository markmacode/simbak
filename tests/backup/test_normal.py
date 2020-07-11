import os
from unittest.mock import patch
from simbak.backup.normal import BackupNormal


@patch('simbak.fileutil.filter_paths')
@patch('simbak.fileutil.unique_file_name')
@patch('simbak.fileutil.create_targz')
@patch('simbak.fileutil.distribute_file')
def test__backup(mock_distribute_file, mock_create_targz,
                 mock_unique_file_name, mock_filter_paths):
    mock_filter_paths.side_effect = [
        [
            os.path.join('first', 'source', 'file.txt'),
            os.path.join('third', 'source', 'another.txt'),
        ],
        [
            os.path.join('first', 'destination'),
            os.path.join('second', 'destination'),
            os.path.join('third', 'destination'),
        ],
    ]
    mock_unique_file_name.return_value = 'hello--1.tar.gz'
    mock_create_targz.return_value = \
        os.path.join('first', 'destination', 'hello--1.tar.gz')

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
    name = 'hello'
    backup_agent = BackupNormal(sources, destinations, name)

    backup_agent.backup()

    mock_create_targz.assert_called_with(
        sources=[
            os.path.join('first', 'source', 'file.txt'),
            os.path.join('third', 'source', 'another.txt'),
        ],
        destination=os.path.join('first', 'destination'),
        file_name='hello--1.tar.gz',
        compression_level=6
    )
    mock_distribute_file.assert_called_with(
        path=os.path.join('first', 'destination', 'hello--1.tar.gz'),
        destinations=[
            os.path.join('second', 'destination'),
            os.path.join('third', 'destination'),
        ],
    )
