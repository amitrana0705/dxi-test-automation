# ODI Test Automation --- Architecture Design

**Status:** Target design. Excel reading and CLI source selection are
the current demo baseline. Jira integration, ODI triggering, monitoring,
validation and issue updates are planned, not yet implemented.

## Objective

Support Excel and Jira as interchangeable sources of ODI test requests.
Normalize the input, resolve approved configuration, execute and monitor
a Load Plan, validate scenarios and data, and produce PASS/FAIL
evidence. For Jira-originated requests, update the same issue.

## Architecture

``` mermaid
flowchart TD
 X[Excel template] --> ER[Excel reader]
 J[Jira issue] --> JR[Jira reader]
 ST[Jira status transition] --> TR[Poller or webhook]
 TR --> JR
 ER --> N[Normalized test request]
 JR --> N
 N --> V[Validate input and resolve config]
 V --> P[Prepare FULL/DELTA test state]
 P --> O[Trigger ODI Load Plan]
 O --> I[Persist execution ID]
 I --> M[Poll Load Plan and Scenario status]
 M --> D{Terminal?}
 D -->|No| W[Wait 2-5 minutes]
 W --> M
 D -->|Failure or timeout| F[Collect diagnostics]
 D -->|Success| A[Data assertions]
 A --> R[PASS/FAIL and evidence]
 F --> R
 R --> U[Report and optional Jira update]
```

## Common request contract

Both readers must return the same structure, independent of Excel
headers and Jira custom-field IDs:

``` json
{
  "request_id": "TC_001",
  "origin": "excel",
  "environment": "CTE",
  "load_plan": "LP_CUSTOMER",
  "source_system": "CUSIS",
  "target_system": "OFP_DB",
  "load_type": "FULL",
  "validation_profile": "customer_default",
  "poll_interval_seconds": 300,
  "timeout_minutes": 360
}
```

Names are illustrative. Reject missing or unapproved values before
execution.

## Component responsibilities

  -----------------------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------------------
  `main.py`                           CLI and orchestration entry point; no
                                      Excel/Jira parsing

  `readers/excel_reader.py`           Read enabled rows in
                                      `test_cases/ODI_Test_Execution_Template.xlsx`

  `readers/jira_reader.py`            Read Jira issue and map custom fields

  `readers/request_reader.py`         Select adapter; return normalized requests

  `triggers/jira_poller.py`           Find eligible requests and claim jobs

  `triggers/webhook.py`               Receive authenticated Jira events; enqueue jobs

  `odi/load_plan_runner.py`           Trigger ODI and persist execution ID

  `odi/execution_monitor.py`          Poll Load Plan/Scenario status, logs and errors

  `validation/`                       Check load strategy, source/target counts and
                                      business rules

  `reporting/`                        Store evidence and update Jira
  -----------------------------------------------------------------------------------

## Configuration separation

-   **Request:** environment, Load Plan, source, target, FULL/DELTA,
    validation profile.
-   **Environment config:** approved ODI endpoints, repository and
    database connection aliases, secret references.
-   **Load Plan config:** expected Scenarios, load strategy, FULL/DELTA
    preparation, registered SQL/filter rules.
-   **Secrets:** environment variables or secret manager, never Jira
    fields, Excel or source control.
-   Never execute arbitrary SQL supplied by a Jira issue. Destructive
    test-state updates (for example setting last-run time to NULL)
    require explicit authorization and test-environment safeguards.

## Jira trigger design

A Jira issue is eligible only if it belongs to the approved project, has
the `odi-automation` label or dedicated issue type, has complete input
fields, and enters configured status `Development` or `In Progress`. Do
not trigger ordinary development tasks.

**Polling:** worker searches Jira at intervals and atomically claims a
run before triggering ODI. JQL/status alone cannot prevent duplicates.

**Webhook:** Jira Automation detects a transition and sends the issue
key to an authenticated HTTPS endpoint. The receiver queues work and
responds promptly; the worker handles multi-hour execution. Jira Cloud
cannot directly call a local-only Python process.

Use a durable run record keyed by issue/request ID and explicit run
number. Save claim owner, state, timestamps, ODI execution ID and
evidence path. On restart, resume monitoring the saved ODI execution ID
rather than retriggering. A deliberate rerun creates a new run number.

Suggested states:
`NEW → VALIDATED → CLAIMED → STARTING → RUNNING → VALIDATING → PASSED / FAILED / TIMED_OUT / ERROR`.

## ODI monitoring and validation

1.  Resolve approved environment and Load Plan settings.
2.  Prepare FULL/DELTA test state and expected source counts.
3.  Trigger ODI; immediately persist execution ID.
4.  Poll ODI API or Work Repository every 2--5 minutes; collect Load
    Plan and Scenario status, progress, errors and counts.
5.  On terminal failure, collect diagnostics; on success, perform
    configured data assertions.
6.  On timeout, report timeout. Do not assume the ODI process was
    cancelled.
7.  Report execution ID, per-Scenario status, expected/actual counts,
    errors, assertion results, final outcome and evidence. Mask
    sensitive data.

ODI API, repository schema, status codes and permissions must be
verified against the installed ODI version.

## Target folder layout

``` text
odi-test-automation/
├── main.py
├── readers/
│   ├── __init__.py
│   ├── excel_reader.py
│   ├── jira_reader.py
│   └── request_reader.py
├── triggers/
│   ├── jira_poller.py
│   └── webhook.py
├── config/
│   ├── environments.yaml
│   └── load_plans.yaml
├── test_cases/
│   └── ODI_Test_Execution_Template.xlsx
├── odi/
│   ├── load_plan_runner.py
│   └── execution_monitor.py
├── validation/
│   ├── scenario_validator.py
│   └── database_validator.py
├── reporting/
│   ├── result_writer.py
│   └── jira_updater.py
├── tests/
├── reports/
├── ARCHITECTURE.md
└── HOW_TO_RUN.md
```

This is a target layout, not a claim that all modules already exist.

## Delivery milestones

1.  Excel reader and `--source` CLI (baseline).
2.  Validate normalized request and test adapter mappings.
3.  Read one Jira issue with `--issue` (read-only).
4.  Trigger ODI and persist execution ID.
5.  Poll long-running execution with timeout/recovery.
6.  Validate Scenario statuses and FULL/DELTA data.
7.  Generate evidence and update Jira.
8.  Add durable Jira polling; optionally webhook and queue.
9.  Deploy to an approved runner with ODI/database network access.
