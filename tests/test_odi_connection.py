from odi.dummy_odi_client import DummyODIClient


def test_odi_connection():

    odi_client = DummyODIClient()

    connected = odi_client.check_connection()

    assert connected is True