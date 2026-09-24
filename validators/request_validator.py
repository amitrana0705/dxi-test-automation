
REQUIRED_FIELDS = [
    "test_case_id",
    "environment",
    "load_plan",
    "source_system",
    "target_system",
    "load_type"
]

VALID_LOAD_TYPES = ["FULL", "DELTA"]

VALID_ENVIRONMENTS = ["DEV", "CTE", "PREPROD"]


def validate_request(test_request):

    errors = []

    # Check mandatory fields
    for field in REQUIRED_FIELDS:

        value = test_request.get(field)

        if value is None or not str(value).strip():
            errors.append(f"Missing required field: {field}")

    # Validate environment
    environment = str(
        test_request.get("environment") or ""
    ).strip().upper()

    if environment and environment not in VALID_ENVIRONMENTS:
        errors.append(
            f"Invalid environment: {environment}"
        )

    # Validate load type
    load_type = str(
        test_request.get("load_type") or ""
    ).strip().upper()

    if load_type and load_type not in VALID_LOAD_TYPES:
        errors.append(
            f"Invalid load type: {load_type}"
        )

    return errors