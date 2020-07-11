from unittest.mock import patch

from simbak import backup


@patch('simbak.agent.normal.NormalAgent.backup')
def test__backup(mock_agent_backup):
    sources = []
    destinations = []
    name = ''

    backup(sources, destinations, name)

    mock_agent_backup.assert_called_once()
