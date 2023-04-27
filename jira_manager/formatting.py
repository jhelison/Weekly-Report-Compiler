from gdocs.elements.text import Text
from gdocs.elements.util import Color, Status
import os

# This is the between gdocs and jira_manager

CHIP_COLOR = Status.NONE.status_to_color()
BACKGROUND_COLOR = Color(255, 217, 61)
TABLE_HEADER = [
    Text().add_text("Assignee").add_color(color=BACKGROUND_COLOR, background=False),
    Text().add_text("Task").add_color(color=BACKGROUND_COLOR, background=False),
    Text().add_text("ETA").add_color(color=BACKGROUND_COLOR, background=False),
    Text().add_text("Status").add_color(color=BACKGROUND_COLOR, background=False),
]


def epic_in_progress_tasks_to_gdocs(tasks_by_epic):
    jira_server = os.getenv("JIRA_SERVER")

    content = {}

    content["headers"] = [0]

    # Prepare the text section
    content["text"] = []

    # Prepare the header
    content["text"].append(
        [
            Text()
            .add_text("Assignee")
            .add_color(color=BACKGROUND_COLOR, background=False),
            Text().add_text("Task").add_color(color=BACKGROUND_COLOR, background=False),
            Text().add_text("ETA").add_color(color=BACKGROUND_COLOR, background=False),
            Text()
            .add_text("Status")
            .add_color(color=BACKGROUND_COLOR, background=False),
        ]
    )

    row_num = 1
    for epic, tasks in tasks_by_epic.items():
        # Add the header
        content["headers"].append(row_num)

        # Add the text
        content["text"].append(
            [
                Text()
                .add_text(" ")
                .add_color(color=BACKGROUND_COLOR, background=False),
                Text()
                .add_text(epic.fields.summary)
                .add_color(color=BACKGROUND_COLOR, background=False),
                Text()
                .add_text(epic.fields.duedate if epic.fields.duedate else " ")
                .add_color(CHIP_COLOR.background)
                .add_color(CHIP_COLOR.foreground, background=False),
                Text()
                .add_text(" ")
                .add_color(color=BACKGROUND_COLOR, background=False),
            ]
        )

        if tasks:
            row_num += 1
            for task in tasks:
                assignee = task.fields.assignee.displayName.split()
                assignee_name = (
                    Text()
                    .add_text(assignee[0] + " " + assignee[-1])
                    .add_color(CHIP_COLOR.background)
                    .add_color(CHIP_COLOR.foreground, background=False)
                )

                issue_link = (
                    Text()
                    .add_text(f"{task.key}: {task.fields.summary}")
                    .add_hyperlink(
                        link=jira_server + "/browse/" + task.key, end=len(task.key)
                    )
                )

                if task.fields.duedate:
                    due_date = (
                        Text()
                        .add_text(task.fields.duedate)
                        .add_color(CHIP_COLOR.background)
                        .add_color(CHIP_COLOR.foreground, background=False)
                    )
                else:
                    due_date = (
                        Text()
                        .add_text("TBD")
                        .add_color(CHIP_COLOR.background)
                        .add_color(CHIP_COLOR.foreground, background=False)
                    )

                status_color = Status(str(task.fields.status).upper()).status_to_color()
                status = (
                    Text()
                    .add_text(str(task.fields.status).upper())
                    .add_color(status_color.background)
                    .add_color(status_color.foreground, background=False)
                )

                content["text"].append([assignee_name, issue_link, due_date, status])
                row_num += 1

    return content


# def epic_task_to_gdocs(epic, tasks):
