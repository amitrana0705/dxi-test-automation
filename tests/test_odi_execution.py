from odi.dummy_odi_client import DummyODIClient


def test_start_load_plan():

    odi_client = DummyODIClient()

    # Check ODI connection
    connected = odi_client.check_connection()
    assert connected is True

    # Start Load Plan
    load_plan_name = "LP_HELENA_HIP_00001_BUSINESSUNIT"

    execution_id = odi_client.start_load_plan(load_plan_name)

    # Verify ODI returned an execution ID
    assert execution_id is not None
    assert execution_id != ""