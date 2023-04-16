from gdocs.tags import Tags
from gdocs.process import apply_date_chip, apply_worked_tasks_table


def handle_start_date_small(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_start_date_big(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_end_date_small(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_end_date_big(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_worked_tasks_table(config: dict, tag: Tags):
    apply_worked_tasks_table(config, tag)


tag_handlers = {
    # Tags.START_DATE_SMALL: handle_start_date_small,
    # Tags.START_DATE_BIG: handle_start_date_big,
    # Tags.END_DATE_SMALL: handle_end_date_small,
    # Tags.END_DATE_BIG: handle_end_date_big,
    Tags.WORKED_TASKS_TABLE: handle_worked_tasks_table,
}


# Handle all the tags at the same time
def handle_tags(config: dict):
    for tag in Tags:
        if tag in tag_handlers:
            tag_handlers[tag](config, tag)
