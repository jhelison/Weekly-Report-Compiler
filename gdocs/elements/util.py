from typing import Union, List, Tuple
from enum import Enum
from dataclasses import dataclass

MAX_COLOR_VALUES = 255


class Color:
    def __init__(self, red: int, green: int, blue: int):
        """
        Represents a color with RGB values.

        Args:
            red (int): The value of the red component of the color (0-255).
            green (int): The value of the green component of the color (0-255).
            blue (int): The value of the blue component of the color (0-255).
        """
        self.red = red
        self.green = green
        self.blue = blue

    def as_color_request(self):
        """
        Returns the color as a request object compatible with Google Docs API.

        Returns:
            dict: The color request object.
        """
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
        """
        Returns the background and foreground colors associated with the status.

        Returns:
            StatusColor: The background and foreground colors associated with the status.
        """
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
    """
    Finds a tag in the Google Docs document content.

    Args:
        tag (str): The tag to search for.
        content (list): The content of the Google Docs document.

    Returns:
        Tuple[Union[int, None], Union[int, None]]: A tuple containing the position of the tag and its length, or (None, None) if the tag is not found.
    """
    location = None
    tag_length = None

    for item in content:
        if "paragraph" in item:
            for element in item["paragraph"]["elements"]:
                text_run = element.get("textRun")
                if text_run and tag in text_run["content"]:
                    location = element["startIndex"] + \
                        text_run["content"].index(tag)
                    tag_length = len(tag)
                    break

    return location, tag_length


# Builds the remove content range for removing tags
# Returns a list of dict with the remove context
def create_remove_content_requests(location: int, tag_length: int) -> List[dict]:
    """
    Builds a list of requests to remove content based on the location and tag length.

    Args:
        location (int): The position of the tag in the document.
        tag_length (int): The length of the tag.

    Returns:
        List[dict]: A list of remove content requests.
    """
    return [
        {
            "deleteContentRange": {
                "range": {"startIndex": location, "endIndex": location + tag_length}
            }
        }
    ]


def add_page_break(location: int) -> List[dict]:
    """
    Builds a list of requests to add a page break at the specified location.

    Args:
        location (int): The position at which to add the page break.

    Returns:
        List[dict]: A list of insert page break requests.
    """
    return [{"insertPageBreak": {"location": {"index": location}}}]
