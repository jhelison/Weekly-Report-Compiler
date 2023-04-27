from enum import Enum


class Tags(Enum):
    # Dates tag
    START_DATE_SMALL = "<start_date_small>"
    START_DATE_BIG = "<start_date_big>"

    END_DATE_SMALL = "<end_date_small>"
    END_DATE_BIG = "<end_date_big>"

    # Table tag
    WORKED_TASKS_TABLE = "<worked_tasks_table>"

    # Worked tasks list
    WORKED_TASKS_LIST = "<worked_tasks_list>"

    MARKDOWN = "<markdown>"
