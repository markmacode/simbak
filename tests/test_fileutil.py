import os
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

from freezegun import freeze_time

from simbak import fileutil


@patch('os.path.exists')
def test__filter_paths__create_false(mock_exists):
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
    actual = fileutil.filter_paths(paths)

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
    actual = fileutil.filter_paths(paths, True)

    assert expected == actual


@freeze_time('2020-01-01 01:01:01')
def test__unique_file_name():
    name = 'hello'

    expected = 'hello--2020-01-01--01-01-01.tar.gz'
    actual = fileutil.unique_file_name(name)

    assert expected == actual


@patch('shutil.copyfile')
def test__distribute_file(mock_copyfile):
    path = os.path.join('path', 'to', 'file.tar.gz')
    destinations = [
        os.path.join('distination', 'one'),
        os.path.join('distination', 'two'),
        os.path.join('distination', 'three'),
    ]

    fileutil.distribute_file(path, destinations)

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


@patch('tarfile.open')
def test__create_targz__happy_path(mock_open):
    mock_tar = Mock()
    mock_open.return_value = mock_tar

    sources = [
        os.path.join('source', 'path', 'one.txt'),
        os.path.join('other', 'path', 'two.txt'),
        os.path.join('another', 'path', 'three'),
    ]
    destination = os.path.join('path', 'to', 'destination')
    file_name = 'hello.tar.gz'

    expected = os.path.join(destination, file_name)
    actual = fileutil.create_targz(sources, destination, file_name)

    assert expected == actual
    mock_tar.assert_has_calls([
        call.add(
            os.path.join('source', 'path', 'one.txt'),
            'one.txt',
        ),
        call.add(
            os.path.join('other', 'path', 'two.txt'),
            'two.txt',
        ),
        call.add(
            os.path.join('another', 'path', 'three'),
            'three',
        ),
    ])


@patch('tarfile.open')
def test__create_targz__permission_error(mock_open):
    mock_tar = Mock()
    mock_tar.add.side_effect = [None, PermissionError(''), None]
    mock_open.return_value = mock_tar

    sources = [
        os.path.join('source', 'path', 'one.txt'),
        os.path.join('other', 'path', 'two.txt'),
        os.path.join('another', 'path', 'three'),
    ]
    destination = os.path.join('path', 'to', 'destination')
    file_name = 'hello.tar.gz'

    expected = os.path.join(destination, file_name)
    actual = fileutil.create_targz(sources, destination, file_name)

    assert expected == actual
    mock_tar.assert_has_calls([
        call.add(
            os.path.join('source', 'path', 'one.txt'),
            'one.txt',
        ),
        call.add(
            os.path.join('other', 'path', 'two.txt'),
            'two.txt',
        ),
        call.add(
            os.path.join('another', 'path', 'three'),
            'three',
        ),
    ])


@patch('tarfile.open')
def test__create_targz__file_exists_error(mock_open):
    mock_tar = Mock()
    mock_open.side_effect = FileExistsError('')

    sources = [
        os.path.join('source', 'path', 'one.txt'),
        os.path.join('other', 'path', 'two.txt'),
        os.path.join('another', 'path', 'three'),
    ]
    destination = os.path.join('path', 'to', 'destination')
    file_name = 'hello.tar.gz'

    expected = os.path.join(destination, file_name)
    actual = fileutil.create_targz(sources, destination, file_name)

    assert expected == actual
    mock_tar.add.assert_not_called()
