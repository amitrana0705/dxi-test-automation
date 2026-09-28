import yaml

from read_jira import read_jira_issue


def extract_jira_fields(description):

    test_config = {}

    for block in description.get("content", []):

        if block.get("type") != "paragraph":
            continue

        text = "".join(
            item.get("text", "")
            for item in block.get("content", [])
            if item.get("type") == "text"
        )

        if " - " not in text:
            continue

        key, value = text.split(" - ", 1)

        key = key.strip().lower().replace(" ", "_")
        value = value.strip()

        test_config[key] = value

    return test_config


def generate_yaml(issue_key):

    issue = read_jira_issue(issue_key)

    description = issue["fields"]["description"]

    test_config = extract_jira_fields(description)

    test_config["jira_key"] = issue_key

    print("Extracted Configuration:")
    print(test_config)

    with open(
        f"{issue_key}.yaml",
        "w",
        encoding="utf-8"
    ) as file:

        yaml.safe_dump(
            test_config,
            file,
            sort_keys=False,
            allow_unicode=True
        )

    print(f"\nYAML generated: {issue_key}.yaml")


if __name__ == "__main__":

    generate_yaml("DDIFS-3786")