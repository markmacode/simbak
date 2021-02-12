from unittest.mock import patch

from simbak import cli


def test__parse_args__short():
    args = [
        '-s', '/source/1', '/source/2',
        '-d', '/destination/1', '/destination/2',
        '-n', 'hello',
        '-c', '6'
    ]
    parsed = cli.parse_args(args)

    assert parsed.source == ['/source/1', '/source/2']
    assert parsed.destination == ['/destination/1', '/destination/2']
    assert parsed.name == 'hello'
    assert parsed.compression_level == 6


def test__parse_args__long():
    args = [
        '--source', '/source/1', '/source/2',
        '--destination', '/destination/1', '/destination/2',
        '--name', 'hello',
        '--compression-level', '6'
    ]
    parsed = cli.parse_args(args)

    assert parsed.source == ['/source/1', '/source/2']
    assert parsed.destination == ['/destination/1', '/destination/2']
    assert parsed.name == 'hello'
    assert parsed.compression_level == 6


@patch('simbak.cli.parse_args')
@patch('simbak.backup')
def test__main(mock_backup, mock_parse_args):
    args = type('obj', (object,), {
        'source': ['source/1', 'source/2'],
        'destination': ['destination/1', 'destination/2'],
        'name': 'hello',
        'compression_level': 6
    })()
    mock_parse_args.return_value = args

    cli.main()

    mock_backup.assert_called_with(
        sources=args.source,
        destinations=args.destination,
        name=args.name,
        compression_level=args.compression_level)
