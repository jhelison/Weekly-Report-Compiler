from jira import JIRA
import os

# Make the login into Jira
def new_jira() -> JIRA:

    jira = JIRA(
        server=os.getenv("JIRA_SERVER"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_TOKEN"))
    )

    return jira
