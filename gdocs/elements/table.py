from gdocs.elements.text import Text
from typing import List


def create_table_request(location: int, content: dict) -> list:
    """Create a batch update request to insert a table with the provided content at the specified location.

    Args:
        location (int): The index location where the table should be inserted.
        content (dict): The content of the table including headers and text.

    Returns:
        list: A list of batch update requests for creating the table.

    """
    requests = []

    num_rows = len(content["text"])
    num_columns = len(content["text"][0])

    # Insert a blank table at the tag location
    requests.append(create_table(location, num_columns, num_rows))

    # Update column sizes
    requests.append(update_table_column_sizes(location, [110, 380, 110, 110]))

    # Build headers
    requests.append(set_headers_style(
        location, num_columns, content["headers"]))

    # Build the final cells text
    request, text_position = set_text(location, content["text"])
    requests.append(request)

    return requests, text_position


def create_table(location: int, num_columns: int, num_rows: int) -> list:
    """Create a batch update request to insert a table at the specified location.

    Args:
        location (int): The index location where the table should be inserted.
        num_columns (int): The number of columns in the table.
        num_rows (int): The number of rows in the table.

    Returns:
        list: A list containing the batch update request for creating the table.

    """
    return [
        [
            {
                "insertTable": {
                    "location": {"index": location},
                    "columns": num_columns,
                    "rows": num_rows,
                },
            }
        ]
    ]


def update_table_column_sizes(location: int, column_widths: list) -> list:
    """Create batch update requests to update the column sizes of a table.

    Args:
        location (int): The index location of the table.
        column_widths (list): The desired widths of the table columns.

    Returns:
        list: A list of batch update requests for updating the column sizes.

    """
    requests = []

    for i, width in enumerate(column_widths):
        requests.append(
            {
                "updateTableColumnProperties": {
                    "tableStartLocation": {"index": location + 1},
                    "columnIndices": [i],
                    "tableColumnProperties": {
                        "widthType": "FIXED_WIDTH",
                        "width": {"magnitude": width, "unit": "PT"},
                    },
                    "fields": "*",
                }
            }
        )

    return requests


def set_headers_style(location: int, num_columns: int, rows_indexes: list) -> list:
    """Create batch update requests to set the style of the table headers.

    Args:
        location (int): The index location of the table.
        num_columns (int): The number of columns in the table.
        rows_indexes (list): The indexes of the rows containing headers.

    Returns:
        list: A list of batch update requests for setting the header style.

    """
    requests = []

    style = {
        "tableCellStyle": {
            "backgroundColor": {
                "color": {
                    "rgbColor": {"red": 10 / 256, "green": 47 / 256, "blue": 68 / 256}
                }
            }
        }
    }

    for row in rows_indexes:
        requests.append(
            [
                {
                    "updateTableCellStyle": {
                        **style,
                        "fields": "*",
                        "tableRange": {
                            "rowSpan": 1,
                            "columnSpan": num_columns,
                            "tableCellLocation": {
                                "columnIndex": 0,
                                "rowIndex": row,
                                "tableStartLocation": {"index": location + 1},
                            },
                        },
                    },
                }
            ]
        )

    return requests


def set_text(location: int, texts: List[List[Text]]) -> list:
    """Create batch update requests to set the text content of the table cells.

    Args:
        location (int): The index location of the table.
        texts (List[List[Text]]): The text content of the table cells.

    Returns:
        list: A list of batch update requests for setting the text content.

    """
    requests = []

    # First position considering table base spacing
    text_position = location + 4
    text_last_position = 0

    for row in texts:
        for text in row:
            text.position = text_position
            requests.append(text.requests)
            text_position = text.last_position + 2

            text_last_position = (
                text.last_position
                if text.last_position > text_last_position
                else text.last_position
            ) + 2
        # Add 1 to jump to the next row
        text_position += 1

    return requests, text_last_position
