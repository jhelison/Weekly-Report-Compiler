from gdocs.elements.util import Status
from gdocs.elements.text import Text
from gdocs.tags import Tags
from gdocs.account import get_document_content, apply_content
from gdocs.elements.table import create_table_request
from gdocs.elements.util import find_tag, create_remove_content_requests, add_page_break
from jira_manager.formatting import epic_in_progress_tasks_to_gdocs
from gdocs.elements.markdown import Markdown, markdown_text, clean_jira_markdown
import jira2markdown
from jira_manager.epic import epic_in_progress, epic_in_progress_tasks, epic_appendix_in_progress
from loguru import logger
import json
import os


def apply_date_chip(
    config: dict,
    tag: Tags,
):
    date_type = None
    size = None
    if tag == tag.START_DATE_SMALL:
        date_type = "start_date"
        size = "small"
    elif tag == tag.START_DATE_BIG:
        date_type = "start_date"
        size = "big"
    elif tag == tag.END_DATE_SMALL:
        date_type = "end_date"
        size = "small"
    elif tag == tag.END_DATE_BIG:
        date_type = "end_date"
        size = "big"

    try:
        doc_content = get_document_content(config["doc"]["document_id"])
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return

        remove_request = create_remove_content_requests(location, tag_length)

        color = Status.NONE.status_to_color()
        chip_request = (
            Text(location)
            .add_text(str(config["doc"][date_type]))
            .add_color(background=True, color=color.background)
            .add_color(background=False, color=color.foreground)
            # .add_font_size(config["style"]["text_size"][size])
            .requests
        )

        final_request = [*remove_request, *chip_request]

        apply_content(config["doc"]["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")
    except Exception as e:
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_worked_tasks_table(config: dict, tag: Tags):
    try:
        doc_content = get_document_content(config["doc"]["document_id"])
        # print(json.dumps(doc_content))
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return
        remove_request = create_remove_content_requests(location, tag_length)

        # Fetch the data, process it and build the table requests
        epics = epic_in_progress()
        tasks_by_epic = epic_in_progress_tasks(epics)
        content = epic_in_progress_tasks_to_gdocs(tasks_by_epic)
        table_request, _ = create_table_request(location, content)

        final_request = [*remove_request, *table_request]

        apply_content(config["doc"]["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_worked_tasks_list(config: dict, tag: Tags):
    try:
        jira_server = os.getenv("JIRA_SERVER")

        doc_content = get_document_content(config["doc"]["document_id"])
        # print(json.dumps(doc_content))
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return
        remove_request = create_remove_content_requests(location, tag_length)

        # Start here:
        epics = epic_in_progress()
        tasks_by_epic = epic_in_progress_tasks(epics)
        requests = []
        for epic, tasks in tasks_by_epic.items():
            # Set the header
            header = (
                Text(location)
                .add_text(f"{epic.key}: {epic.fields.summary}")
                .add_heading(1)
                .add_hyperlink(
                    link=jira_server + "/browse/" + epic.key,
                    end=location + len(epic.key),
                )
            )
            requests.append(header.requests)
            location = header.last_position

            # Add a new line
            request, location = Text.new_line(location)
            requests.append(request)

            # Add the roadmap text
            road_map_text = (
                Text(location)
                .add_text("Here's the roadmap for the epic:")
                .add_heading(0)
            )
            requests.append(road_map_text.requests)
            location = road_map_text.last_position

            # Set the new table
            content = epic_in_progress_tasks_to_gdocs({epic: tasks})
            table_request, text_position = create_table_request(
                location, content)
            requests.append(table_request)
            location = text_position

            if epic.fields.__dict__.get(config["jira"]["epic_weekly_report_field"]):
                # Add the epic wr notes
                markdown = Markdown(
                    location,
                    clean_jira_markdown(jira2markdown.convert(
                        epic.fields.__dict__.get(
                            config["jira"]["epic_weekly_report_field"]
                        ))
                    ),
                )
                requests.append(markdown.process())
                location = markdown.position

                # Add a new line
                request, location = Text.new_line(location)
                requests.append(request)

            # Check if at least one task has notes
            has_notes = False
            for task in tasks:
                wr_note = task.fields.__dict__.get(
                    config["jira"]["task_weekly_report_field"]
                )
                if wr_note:
                    has_notes = True

            # Only set the develop progress header is tasks has notes

            if has_notes:
                # Set the development progress header
                header = Text(location).add_text(
                    "Current development").add_heading(2)
                requests.append(header.requests)
                location = header.last_position

                # Add a new line
                request, location = Text.new_line(location)
                requests.append(request)

            for task in tasks:
                wr_note = task.fields.__dict__.get(
                    config["jira"]["task_weekly_report_field"]
                )

                if not wr_note or str(task.fields.status).upper() == "DONE":
                    continue

                # Set the task tittle
                header = (
                    Text(location)
                    .add_text(f"{task.key}: {task.fields.summary}")
                    .add_heading(3)
                    .add_hyperlink(
                        link=jira_server + "/browse/" + task.key,
                        end=location + len(task.key),
                    )
                )
                requests.append(header.requests)
                location = header.last_position

                # Add a new line
                request, location = Text.new_line(location)
                requests.append(request)

                # Add the weekly report note
                markdown = Markdown(location, clean_jira_markdown(
                    jira2markdown.convert(wr_note)))
                requests.append(markdown.process())
                location = markdown.position

            # Add a final page break
            requests.append(*add_page_break(location))
            location += 1

        final_request = [*remove_request, *requests]

        apply_content(config["doc"]["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        raise e
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_appendix_tasks_list(config: dict, tag: Tags):
    try:
        jira_server = os.getenv("JIRA_SERVER")

        doc_content = get_document_content(config["doc"]["document_id"])
        # print(json.dumps(doc_content))
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return
        remove_request = create_remove_content_requests(location, tag_length)

        # Start here:
        epics = epic_appendix_in_progress()
        tasks_by_epic = epic_in_progress_tasks(epics)
        requests = []
        for epic, tasks in tasks_by_epic.items():
            # Set the header
            header = (
                Text(location)
                .add_text(f"{epic.key}: {epic.fields.summary}")
                .add_heading(3)
                .add_hyperlink(
                    link=jira_server + "/browse/" + epic.key,
                    end=location + len(epic.key),
                )
            )
            requests.append(header.requests)
            location = header.last_position

            # Set the new table
            content = epic_in_progress_tasks_to_gdocs({epic: tasks})
            table_request, text_position = create_table_request(
                location, content)
            requests.append(table_request)
            location = text_position

            # Add a new line
            request, location = Text.new_line(location)
            requests.append(request)

        final_request = [*remove_request, *requests]

        apply_content(config["doc"]["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        raise e
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_markdown(config: dict, tag: Tags):
    try:
        doc_content = get_document_content(config["doc"]["document_id"])
        location, tag_length = find_tag(tag.value, doc_content)

        location = 1
        # if location is None:
        #     logger.warning(f"Tag {tag.value} not found on document")
        #     return

        # remove_request = create_remove_content_requests(location, tag_length)

        # Fetch the data, process it and build the table requests
        requests = Markdown(location, markdown_text).process()

        # final_request = [*remove_request, *requests]
        final_request = [*requests]

        apply_content(config["doc"]["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        raise e
        logger.error(f"Error when processing tag {tag.value}, error {e}")
