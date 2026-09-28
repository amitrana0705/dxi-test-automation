from odi.odi_client import ODIClient


class DummyODIClient(ODIClient):
    """
    Dummy ODI implementation used until real ODI
    connectivity is available.
    """

    def check_connection(self) -> bool:
        print("Connecting to Dummy ODI...")
        return True

    def start_load_plan(self, load_plan_name: str) -> str:
        print(f"Starting ODI Load Plan: {load_plan_name}")

        execution_id = "ODI_EXEC_10001"

        print(f"Load Plan started successfully.")
        print(f"Execution ID: {execution_id}")

        return execution_id