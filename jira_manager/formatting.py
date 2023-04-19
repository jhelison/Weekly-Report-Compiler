from gdocs.elements.text import SimpleText, TableHeaderText, ChipText, TextWithLink
from jira_manager.epic import epic_in_progress_tasks
import os

# This is the between gdocs and jira_manager

TABLE_HEADER = [
    TableHeaderText("Assignee"),
    TableHeaderText("Task"),
    TableHeaderText("ETA"),
    TableHeaderText("Status"),
]


def epic_in_progress_tasks_to_gdocs():
    tasks_by_epic = epic_in_progress_tasks()
    jira_server = os.getenv("JIRA_SERVER")

    content = {}

    content["headers"] = [0]

    # Prepare the text section
    content["text"] = [TABLE_HEADER]

    row_num = 1
    for epic, tasks in tasks_by_epic.items():
        # Add the header
        content["headers"].append(row_num)

        # Add the text
        content["text"].append(
            [
                TableHeaderText(" "),
                TableHeaderText(epic.fields.summary),
                ChipText(epic.fields.duedate),
                TableHeaderText(" "),
            ]
        )

        if tasks:
            row_num += 1
            for task in tasks:
                assignee = task.fields.assignee.displayName.split()
                assignee_name = ChipText(assignee[0] + " " + assignee[-1])
                issue_link = TextWithLink(
                    text=task.key,
                    link=jira_server + "/browse/" + task.key,
                    remaining_text=": " + task.fields.summary,
                )

                if task.fields.duedate:
                    due_date = ChipText(task.fields.duedate)
                else:
                    due_date = ChipText("TBD")

                status = ChipText(str(task.fields.status).upper())

                content["text"].append([assignee_name, issue_link, due_date, status])
                row_num += 1

    content["num_columns"] = len(TABLE_HEADER)
    content["num_rows"] = len(content["text"])

    return content
