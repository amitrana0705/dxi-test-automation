# ODI Test Automation --- How to Run

**Current vs planned:** Excel CLI reading is the present demo. Jira
issue CLI, polling, webhook, ODI execution and reporting are planned
interfaces until implemented.

## Getting started --- new developer setup

### Prerequisites

-   Clone or obtain the project repository and open a PowerShell
    terminal in `odi-test-automation/`.
-   Install a supported Python version (check `requires-python` in
    `pyproject.toml`).
-   Install `uv` for the preferred setup, or use Python and pip.
-   Ensure `test_cases/ODI_Test_Execution_Template.xlsx` exists and its
    `Test_Cases` worksheet matches the reader's expected headers.
-   Obtain approved DEV repository connection details and ODI
    command-line utility information from the Platform Team when working
    on ODI integration. These are not required just to read the Excel
    template.

### Option A --- uv (preferred)

For an existing checkout containing `pyproject.toml` and `uv.lock`,
install the project's locked dependencies:

``` powershell
uv sync
```

Run the current Excel demo:

``` powershell
uv run python main.py --source excel
```

Run the tests:

``` powershell
uv run pytest -v
```

If the required dependencies have not yet been added to the project, the
project maintainer can add them once:

``` powershell
uv add openpyxl oracledb python-dotenv pyyaml
uv add --dev pytest
```

`openpyxl` reads Excel; `oracledb` connects to the Oracle repository;
`python-dotenv` loads local environment settings; `pyyaml` reads YAML
configuration; and `pytest` runs tests. The ODI command-line utility is
provided separately by the Platform Team, not installed with pip.

### Option B --- standard Python and pip

From the project root, create and activate a virtual environment:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the exported dependencies and run the Excel demo:

``` powershell
python -m pip install -r requirements.txt
python main.py --source excel
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe`
directly instead of changing system-wide execution policy.

### Maintaining the dependency files

`pyproject.toml` and `uv.lock` are the primary dependency definitions.
After adding or changing a dependency, regenerate the pip-compatible
file:

``` powershell
uv export --format requirements-txt --all-groups --no-hashes --output-file requirements.txt
```

`--all-groups` includes the development group, including `pytest`, for
contributors. Commit `pyproject.toml`, `uv.lock`, and `requirements.txt`
together. Other developers should use `uv sync` rather than repeatedly
running `uv add` on a freshly cloned project.

### Local configuration and secrets

Create a local `.env` only when you start repository/Jira integration.
Obtain real connection settings through approved channels; never commit
credentials. A safe `.env.example` may document variable names with
placeholder values. Ensure `.gitignore` includes:

``` gitignore
.venv/
.env
__pycache__/
.pytest_cache/
*.pyc
reports/
```

Commit `ARCHITECTURE.md` and `HOW_TO_RUN.md` so the team can follow the
same setup and execution guidance.

## Option 1 --- Excel demo (current)

``` powershell
uv run python main.py --source excel
```

Or use the default:

``` powershell
uv run python main.py
```

This currently prints enabled normalized test requests; it does **not**
yet trigger ODI. Set `Enabled` to `YES` in the workbook. Verify
`readers/request_reader.py` points to
`ODI_Test_Execution_Template.xlsx`.

Help and argument validation:

``` powershell
uv run python main.py --help
uv run python main.py --source database
```

The second command should reject an unsupported source.

## Option 2 --- One Jira issue (planned)

Once the Jira adapter and `--issue` argument exist:

``` powershell
uv run python main.py --source jira --issue ODIAUTO-125
```

Today, `--issue` may be unrecognized and `jira_reader.py` may raise
`NotImplementedError`. The future adapter reads the issue, validates its
fields and returns the same request structure as Excel.

Example non-secret settings:

``` text
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_PROJECT_KEY=ODIAUTO
```

Use approved service-account credentials via environment variables or
secret manager; never put tokens in Jira issues or Excel.

## Option 3 --- Jira status polling (planned)

A worker periodically queries eligible issues, claims them durably, and
executes them. Illustrative JQL:

``` jql
project = ODIAUTO
AND labels = "odi-automation"
AND status in ("Development", "In Progress")
ORDER BY created ASC
```

Proposed command after implementation:

``` powershell
uv run python -m triggers.jira_poller
```

This is not an existing command yet. A status match alone must never
start duplicate ODI executions.

## Option 4 --- Jira Automation webhook (planned)

Create an Automation rule on transition to `Development` or
`In Progress`; require approved project, ODI issue type/label and
complete fields. Send an authenticated HTTPS request containing an issue
key:

``` json
{"issue_key": "ODIAUTO-125", "event": "ODI_TEST_REQUEST"}
```

A reachable Python endpoint validates the event, queues the job and
responds promptly. A background worker reads Jira and runs ODI. Do not
keep an HTTP request open for hours; Jira Cloud cannot reach your
machine's localhost directly.

## Option 5 --- CI or scheduled regression (planned)

An approved build agent/scheduler invokes the same runner with Excel or
Jira input. The agent must have network access to the approved ODI and
database endpoints, plus secure access to credentials.

## Future ODI execution sequence

Resolve config → prepare FULL/DELTA state → trigger Load Plan → persist
execution ID → poll every 2--5 minutes → check Load Plan/Scenario status
→ validate counts/data → PASS/FAIL evidence → update Jira if applicable.

Example configurable values:

``` yaml
poll_interval_seconds: 300
timeout_minutes: 360
```

Timeout does not mean ODI was automatically cancelled.

## Troubleshooting

  ---------------------------------------------------------------------
  Symptom                            Check
  ---------------------------------- ----------------------------------
  Excel file not found               Exact workbook name and
                                     `test_cases/` location

  Missing `openpyxl`                 `uv add openpyxl`

  Column `KeyError`                  `Test_Cases` header names

  No test cases                      `Enabled` values

  Jira `NotImplementedError`         Jira adapter is still a
                                     placeholder

  `--issue` unrecognized             Jira CLI not implemented

  Duplicate ODI execution            Durable claim and explicit rerun
                                     ID

  Long run times out                 Poll interval, timeout, execution
                                     ID and ODI status

  Jira update fails                  Service account permissions and
                                     evidence storage
  ---------------------------------------------------------------------

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details.
