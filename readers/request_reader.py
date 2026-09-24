
from pathlib import Path

from readers.excel_reader import read_excel_requests
from readers.jira_reader import read_jira_requests


def get_test_requests(source):

    source = source.strip().lower()

    if source == "excel":

        excel_path = (
            Path(__file__).resolve().parent.parent
            / "test_cases"
            / "ODI_Test_Execution_Template.xlsx"
        )

        return read_excel_requests(excel_path)

    elif source == "jira":

        return read_jira_requests()

    else:

        raise ValueError(
            f"Unsupported request source: {source}"
        )
