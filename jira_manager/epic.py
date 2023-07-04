from jira_manager.account import new_jira
from config.config import get_config


# Get all the epics in "Work in Progress" status
def epic_in_progress():
    jira = new_jira()

    epic_in_progress_jql = get_config()["jira"]["jql"]["epic_in_progress"]

    return jira.search_issues(
        epic_in_progress_jql.format(
            get_config()["jira"]["project"],
            get_config()["jira"]["epic_order_field"].split("_")[-1],
        )
    )

# Get all the epics in "Work in Progress" status


def epic_appendix_in_progress():
    jira = new_jira()

    appendix_tasks_list_jql = get_config()["jira"]["jql"]["appendix_task_list"]

    return jira.search_issues(
        appendix_tasks_list_jql.format(
            get_config()["jira"]["project"],
            get_config()["jira"]["epic_order_field"].split("_")[-1],
        )
    )


def epic_in_progress_tasks(epics):
    jira = new_jira()

    epic_tasks_jql = get_config()["jira"]["jql"]["epic_tasks"]

    # Organize tasks by epic
    tasks_by_epic = {}
    for epic in epics:
        tasks = jira.search_issues(epic_tasks_jql.format(epic.key))
        tasks_by_epic[epic] = tasks

    return tasks_by_epic
