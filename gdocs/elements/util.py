from typing import Union, List, Tuple
from enum import Enum
from dataclasses import dataclass

MAX_COLOR_VALUES = 255


class Color:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def as_color_request(self):
        return {
            "color": {
                "rgbColor": {
                    "red": self.red / MAX_COLOR_VALUES,
                    "green": self.green / MAX_COLOR_VALUES,
                    "blue": self.blue / MAX_COLOR_VALUES,
                }
            }
        }


@dataclass
class StatusColor:
    background: Color
    foreground: Color


class Status(Enum):
    # Dates tag
    TODO = "TO DO"
    WIP = "IN PROGRESS"
    HALTED = "HALTED"
    REVIEW = "REVIEW"
    DONE = "DONE"
    NONE = None

    def status_to_color(self):
        if self == Status.TODO:
            return StatusColor(
                foreground=Color(71, 56, 33), background=Color(255, 229, 160)
            )
        if self == Status.WIP:
            return StatusColor(
                foreground=Color(12, 85, 169), background=Color(191, 225, 246)
            )
        if self == Status.REVIEW:
            return StatusColor(
                foreground=Color(211, 211, 211), background=Color(61, 61, 61)
            )
        if self == Status.DONE:
            return StatusColor(
                foreground=Color(38, 128, 87), background=Color(212, 237, 188)
            )

        return StatusColor(foreground=Color(0, 0, 0), background=Color(229, 229, 229))


# Find a tag on the google docs document
# Returns the position and the tag_length
def find_tag(tag: str, content: list) -> Tuple[Union[int, None], Union[int, None]]:
    location = None
    tag_length = None

    for item in content:
        if "paragraph" in item:
            for element in item["paragraph"]["elements"]:
                text_run = element.get("textRun")
                if text_run and tag in text_run["content"]:
                    location = element["startIndex"] + text_run["content"].index(tag)
                    tag_length = len(tag)
                    break

    return location, tag_length


# Builds the remove content range for removing tags
# Returns a list of dict with the remove context
def create_remove_content_requests(location: int, tag_length: int) -> List[dict]:
    return [
        {
            "deleteContentRange": {
                "range": {"startIndex": location, "endIndex": location + tag_length}
            }
        }
    ]
