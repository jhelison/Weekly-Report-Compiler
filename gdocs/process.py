from gdocs.elements.util import Status
from gdocs.elements.text import Text
from gdocs.tags import Tags
from gdocs.account import get_document_content, apply_content
from gdocs.elements.table import create_table_request
from gdocs.elements.util import find_tag, create_remove_content_requests
from jira_manager.formatting import epic_in_progress_tasks_to_gdocs
from loguru import logger
import json


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
        doc_content = get_document_content(config["document_id"])
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return

        remove_request = create_remove_content_requests(location, tag_length)

        color = Status.NONE.status_to_color()
        chip_request = (
            Text(location)
            .add_text(str(config["dates"][date_type]))
            .add_color(background=True, color=color.background)
            .add_color(background=False, color=color.foreground)
            .add_font_size(config["style"]["text_size"][size])
            .requests
        )

        final_request = [*remove_request, *chip_request]

        apply_content(config["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")
    except Exception as e:
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_worked_tasks_table(config: dict, tag: Tags):
    try:
        doc_content = get_document_content(config["document_id"])
        # print(json.dumps(doc_content))
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return

        content = epic_in_progress_tasks_to_gdocs()

        remove_request = create_remove_content_requests(location, tag_length)
        table_request = create_table_request(location, content)

        final_request = [*remove_request, *table_request]

        apply_content(config["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        # raise e
        logger.error(f"Error when processing tag {tag.value}, error {e}")


def apply_worked_tasks_list(config: dict, tag: Tags):
    try:
        doc_content = get_document_content(config["document_id"])
        # print(json.dumps(doc_content))
        location, tag_length = find_tag(tag.value, doc_content)

        if location is None:
            logger.warning(f"Tag {tag.value} not found on document")
            return

        content = epic_in_progress_tasks_to_gdocs()

        remove_request = create_remove_content_requests(location, tag_length)
        table_request = create_table_request(location, content)

        final_request = [*remove_request, *table_request]

        apply_content(config["document_id"], final_request)
        logger.success(f"Tag {tag.value} replaced with success")

    except Exception as e:
        logger.error(f"Error when processing tag {tag.value}, error {e}")
