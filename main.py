
import argparse

from readers.request_reader import get_test_requests
from validators.request_validator import validate_request

def main():

    # Create command-line argument parser
    parser = argparse.ArgumentParser(
        description="ODI Test Automation Framework"
    )

    # Define input source argument
    parser.add_argument(
        "--source",
        choices=["excel", "jira"],
        default="excel",
        help="Select test request source (excel or jira)"
    )

    # Read command-line arguments
    args = parser.parse_args()

    # Retrieve test requests
    test_requests = get_test_requests(args.source)

    print(f"\nInput Source: {args.source.upper()}")
    print(f"Total Test Requests: {len(test_requests)}")

    for test in test_requests:

        print(f"\nValidating: {test['test_case_id']}")

        errors = validate_request(test)

        if errors:

            print("VALIDATION FAILED")

            for error in errors:
                print(f" - {error}")

            continue

        print("VALIDATION PASSED")

        print("Environment:", test["environment"])
        print("Load Plan:", test["load_plan"])
        print("Source:", test["source_system"])
        print("Target:", test["target_system"])
        print("Load Type:", test["load_type"])


if __name__ == "__main__":
    main()
