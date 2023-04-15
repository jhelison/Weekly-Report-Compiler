from gdocs.tags import Tags
from gdocs.process import apply_date_chip


def handle_start_date_small(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_start_date_big(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_end_date_small(config: dict, tag: Tags):
    apply_date_chip(config, tag)


def handle_end_date_big(config: dict, tag: Tags):
    apply_date_chip(config, tag)


tag_handlers = {
    Tags.START_DATE_SMALL: handle_start_date_small,
    Tags.START_DATE_BIG: handle_start_date_big,
    Tags.END_DATE_SMALL: handle_end_date_small,
    Tags.END_DATE_BIG: handle_end_date_big,
}


# Handle all the tags at the same time
def handle_tags(config: dict):
    for tag in Tags:
        if tag in tag_handlers:
            tag_handlers[tag](config, tag)
