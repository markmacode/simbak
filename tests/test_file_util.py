import os
from unittest.mock import patch
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
