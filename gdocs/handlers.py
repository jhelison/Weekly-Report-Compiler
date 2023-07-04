from gdocs.process import (
    apply_date_chip,
    apply_worked_tasks_table,
    apply_worked_tasks_list,
    apply_appendix_tasks_list
)
from gdocs.tags import Tags


def handle_start_date_small(config: dict, tag: Tags):
    """Handle the start date small tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The start date small tag.
    """
    apply_date_chip(config, tag)


def handle_start_date_big(config: dict, tag: Tags):
    """Handle the start date big tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The start date big tag.
    """
    apply_date_chip(config, tag)


def handle_end_date_small(config: dict, tag: Tags):
    """Handle the end date small tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The end date small tag.
    """
    apply_date_chip(config, tag)


def handle_end_date_big(config: dict, tag: Tags):
    """Handle the end date big tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The end date big tag.
    """
    apply_date_chip(config, tag)


def handle_worked_tasks_table(config: dict, tag: Tags):
    """Handle the worked tasks table tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The worked tasks table tag.
    """
    apply_worked_tasks_table(config, tag)


def handle_worked_tasks_list(config: dict, tag: Tags):
    """Handle the worked tasks list tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The worked tasks list tag.
    """
    apply_worked_tasks_list(config, tag)


def handle_appendix_tasks_list(config: dict, tag: Tags):
    """Handle the appendix tasks list tag.

    Args:
        config (dict): Configuration data.
        tag (Tags): The appendix tasks list tag.
    """
    apply_appendix_tasks_list(config, tag)


tag_handlers = {
    Tags.START_DATE_SMALL: handle_start_date_small,
    Tags.START_DATE_BIG: handle_start_date_big,
    Tags.END_DATE_SMALL: handle_end_date_small,
    Tags.END_DATE_BIG: handle_end_date_big,
    Tags.WORKED_TASKS_TABLE: handle_worked_tasks_table,
    Tags.WORKED_TASKS_LIST: handle_worked_tasks_list,
    Tags.APPENDIX_TASKS_LIST: handle_appendix_tasks_list,
}


# Handle all the tags at the same time
def handle_tags(config: dict):
    """Handle all the tags in the configuration.

    Args:
        config (dict): Configuration data.
    """
    for tag in Tags:
        if tag in tag_handlers:
            tag_handlers[tag](config, tag)
