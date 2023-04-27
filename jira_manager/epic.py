from jira_manager.account import new_jira
from jira_manager.jql import EPIC_IN_PROGRESS_JQL, EPIC_TASKS_JQL
from config.config import get_config


# Get all the epics in "Work in Progress" status
def epic_in_progress():
    jira = new_jira()
    return jira.search_issues(
        EPIC_IN_PROGRESS_JQL.format(
            get_config()["jira"]["project"],
            get_config()["jira"]["epic_order_field"].split("_")[-1],
        )
    )


def epic_in_progress_tasks():
    jira = new_jira()
    epics = epic_in_progress()

    # Organize tasks by epic
    tasks_by_epic = {}
    for epic in epics:
        tasks = jira.search_issues(EPIC_TASKS_JQL.format(epic.key))
        tasks_by_epic[epic] = tasks

    return tasks_by_epic
