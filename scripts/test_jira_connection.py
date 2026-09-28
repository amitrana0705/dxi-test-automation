import os

import httpx
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
JIRA_EMAIL = os.environ["JIRA_EMAIL"]
JIRA_TOKEN = os.environ["JIRA_API_TOKEN"]

url = f"{JIRA_URL}/rest/api/3/myself"

response = httpx.get(
    url,
    auth=(JIRA_EMAIL, JIRA_TOKEN),
    headers={"Accept": "application/json"},
    timeout=30,
)

print("HTTP Status:", response.status_code)

if response.status_code == 200:
    user = response.json()

    print("Authentication successful!")
    print("Display Name:", user.get("displayName"))
    print("Account ID:", user.get("accountId"))

else:
    print("Authentication failed.")
    print("Response:", response.text[:1000])