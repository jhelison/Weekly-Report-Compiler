from gdocs.elements.text import Text
from typing import List

# content = {
#     "headers": [0, 1],
#     "text": [
#         [
#             TableHeaderText("Assignee"),
#             TableHeaderText("Task"),
#             TableHeaderText("ETA"),
#             TableHeaderText("Status"),
#         ],
#         [
#             TableHeaderText(" "),
#             TableHeaderText("EVMOS FORK - MILESTONE 1"),
#             ChipText("2023-01-01"),
#             TableHeaderText(" "),
#         ],
#         [
#             ChipText("Jhelison"),
#             TextWithLink(
#                 "CAYAG-45",
#                 "https://brickabode-internal.atlassian.net/browse/CAYAG-40",
#                 ": [Evmos] Standalone to consumer chain",
#             ),
#             ChipText("2023-01-01"),
#             SimpleText("TODO"),
#         ],
#         [
#             ChipText("Jhelison"),
#             TextWithLink(
#                 "CAYAG-46",
#                 "https://brickabode-internal.atlassian.net/browse/CAYAG-46",
#                 ": [Evmos] Renaming to Ethos",
#             ),
#             ChipText("2020-12-12"),
#             SimpleText("WIP"),
#         ],
#     ],
#     "num_columns": 4,
#     "num_rows": 4,
# }


def create_table_request(location: int, content: dict) -> list:
    requests = []

    num_rows = len(content["text"])
    num_columns = len(content["text"][0])

    # Insert a blank table at the tag location
    requests.append(create_table(location, num_columns, num_rows))

    # Update column sizes
    requests.append(update_table_column_sizes(location, [110, 380, 110, 110]))

    # Build headers
    requests.append(set_headers_style(location, num_columns, content["headers"]))

    # Build the final cells text
    requests.append(set_text(location, content["text"]))

    return requests


def create_table(location: int, num_columns: int, num_rows: int) -> list:
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
    requests = []

    # First position considering table base spacing
    text_position = location + 4

    for row in texts:
        for text in row:
            text.position = text_position
            requests.append(text.requests)
            text_position = text.last_position + 2
        # Add 1 to jump to the next row
        text_position += 1

    # print(requests)

    return requests
