from enum import Enum


class Tags(Enum):
    """Enumeration of tags used in the application."""

    START_DATE_SMALL = "<start_date_small>"
    """Start date small tag."""

    START_DATE_BIG = "<start_date_big>"
    """Start date big tag."""

    END_DATE_SMALL = "<end_date_small>"
    """End date small tag."""

    END_DATE_BIG = "<end_date_big>"
    """End date big tag."""

    WORKED_TASKS_TABLE = "<worked_tasks_table>"
    """Worked tasks table tag."""

    WORKED_TASKS_LIST = "<worked_tasks_list>"
    """Worked tasks list tag."""

    APPENDIX_TASKS_LIST = "<appendix_tasks_list>"
    """Appendix tasks list tag."""
