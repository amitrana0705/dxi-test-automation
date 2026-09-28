import os

import httpx
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.environ["JIRA_BASE_URL"]
JIRA_EMAIL = os.environ["JIRA_EMAIL"]
JIRA_TOKEN = os.environ["JIRA_API_TOKEN"]
ISSUE_KEY = os.getenv("JIRA_ISSUE_KEY", "DDIFS-3786")


def read_jira_issue(issue_key):

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"

    response = httpx.get(
        url,
        auth=(JIRA_EMAIL, JIRA_TOKEN),
        headers={"Accept": "application/json"},
        params={
            "fields": "summary,description,status,issuetype"
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    issue = read_jira_issue(ISSUE_KEY)

    print("Issue Key:", issue["key"])

    print("Summary:", issue["fields"]["summary"])

    print("Status:", issue["fields"]["status"]["name"])

    print("Description:", issue["fields"]["description"])