import os
from unittest.mock import patch
from unittest.mock import call

from freezegun import freeze_time

from simbak import file_util


@patch('os.path.exists')
def test__filter_paths__standard(mock_exists):
    mock_exists.side_effect = [
        True,
        False,
        True,
    ]
    paths = [
        os.path.join('base', 'path', 'file.txt'),
        os.path.join('other', 'path', 'other.txt'),
        os.path.join('another', 'path', 'another.txt'),
    ]

    expected = [
        os.path.join('base', 'path', 'file.txt'),
        os.path.join('another', 'path', 'another.txt'),
    ]
    actual = file_util.filter_paths(paths)

    assert expected == actual


@patch('os.path.exists')
@patch('os.makedirs')
def test__filter_paths__create_true(mock_makedirs, mock_exists):
    mock_exists.side_effect = [
        True,
        False,
        True,
    ]
    mock_makedirs.return_value = None
    paths = [
        os.path.join('base', 'path', 'file.txt'),
        os.path.join('other', 'path', 'other.txt'),
        os.path.join('another', 'path', 'another.txt'),
    ]

    expected = [
        os.path.join('base', 'path', 'file.txt'),
        os.path.join('other', 'path', 'other.txt'),
        os.path.join('another', 'path', 'another.txt'),
    ]
    actual = file_util.filter_paths(paths, True)

    assert expected == actual


@freeze_time('2020-01-01 01:01:01')
def test__unique_file_name():
    name = 'hello'

    expected = 'hello--2020-01-01--01-01-01.tar.gz'
    actual = file_util.unique_file_name(name)

    assert expected == actual


@patch('shutil.copyfile')
def test__distribute_file(mock_copyfile):
    path = os.path.join('path', 'to', 'file.tar.gz')
    destinations = [
        os.path.join('distination', 'one'),
        os.path.join('distination', 'two'),
        os.path.join('distination', 'three'),
    ]

    file_util.distribute_file(path, destinations)

    mock_copyfile.assert_has_calls([
        call(
            os.path.join('path', 'to', 'file.tar.gz'),
            os.path.join('distination', 'one', 'file.tar.gz'),
        ),
        call(
            os.path.join('path', 'to', 'file.tar.gz'),
            os.path.join('distination', 'two', 'file.tar.gz'),
        ),
        call(
            os.path.join('path', 'to', 'file.tar.gz'),
            os.path.join('distination', 'three', 'file.tar.gz'),
        ),
    ])
