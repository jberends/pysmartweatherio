from pathlib import Path

from pysmartweatherio import SmartWeather


def test_client_retrieves_env():
    """
    Client retrieves .env file from root directory and PAT is read
    """
    env_path = Path(Path(__file__).parent.parent / ".env.template")
    client: SmartWeather = SmartWeather.from_env(env_path)

    assert isinstance(client, SmartWeather)
    assert hasattr(client, "_api_key")
    assert client._api_key is not None
    assert hasattr(client, "_station_id")
    assert client._station_id is not None
    assert hasattr(client, "_to_units")
    assert client._to_units is not None
    assert hasattr(client, "_to_units_wind")
    assert client._to_units_wind is not None

