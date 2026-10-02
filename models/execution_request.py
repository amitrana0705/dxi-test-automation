# models/execution_request.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionRequest:
    """
    Normalized technical execution request.

    This model represents the reviewed technical Jira sub-task
    that is consumed by the automation framework.

    The parent business request is intentionally not used
    as the automation input.
    """

    # Jira identification
    issue_key: str
    parent_issue_key: Optional[str]

    # Routing
    technology: str
    environment: str

    # Integration details
    service: str
    source_system: Optional[str] = None
    target_system: Optional[str] = None

    # Execution details
    executable_name: Optional[str] = None
    load_type: Optional[str] = None
    processing_period: Optional[str] = None

    # Request metadata
    requested_by: Optional[str] = None
    notification_email: Optional[str] = None