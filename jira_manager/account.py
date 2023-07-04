from jira import JIRA
import os


def new_jira() -> JIRA:
    """Create a new JIRA instance and authenticate using the provided credentials.

    Returns:
        JIRA: JIRA instance with authentication.
    """

    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_TOKEN"))
    )

    return jira
