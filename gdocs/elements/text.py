from typing import Type
from gdocs.elements.util import Color


class Text:
    def __init__(self, position=0, requests=[], last_position=0):
        """Initialize a Text object.

        Args:
            position (int): The starting position of the text.
            requests (list, optional): List of requests for the text. Defaults to an empty list.
            last_position (int, optional): The last position of the text. Defaults to 0.
        """
        self._position = position
        self._requests = requests
        self._last_position = last_position

    @property
    def position(self):
        """Get the starting position of the text.

        Returns:
            int: The starting position of the text.
        """
        return self._position

    @position.setter
    def position(self, value):
        """Set the starting position of the text and update the requests accordingly.

        Args:
            value (int): The new starting position of the text.
        """
        delta = value - self._position

        new_request = self._requests
        for request in new_request:
            if "insertText" in request:
                request["insertText"]["location"]["index"] += delta
            elif "updateTextStyle" in request:
                request["updateTextStyle"]["range"]["startIndex"] += delta
                request["updateTextStyle"]["range"]["endIndex"] += delta

        self._position += delta
        self._last_position += delta
        self._requests = new_request

    @property
    def last_position(self):
        """Get the last position of the text.

        Returns:
            int: The last position of the text.
        """
        return self._last_position

    @property
    def requests(self):
        """Get the list of requests for the text.

        Returns:
            list: List of requests for the text.
        """
        return self._requests

    def add_text(self, text) -> Type["Text"]:
        """Add text to the text object.

        Args:
            text (str): The text to be added.

        Returns:
            Type["Text"]: A new Text object with the added text.
        """
        request = {
            "insertText": {
                "location": {"index": self.position},
                "text": text,
            }
        }

        self._last_position = self.position + len(text)

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_font_size(
        self, font_size: int, start: int = None, end: int = None
    ) -> Type["Text"]:
        """Add font size to the text.

        Args:
            font_size (int): The font size to be added.
            start (int, optional): The starting position of the text to apply the font size to. Defaults to None.
            end (int, optional): The ending position of the text to apply the font size to. Defaults to None.

        Returns:
            Type["Text"]: A new Text object with the added font size.
        """
        request = {
            "updateTextStyle": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "textStyle": {
                    "fontSize": {"magnitude": font_size, "unit": "PT"},
                },
                "fields": "fontSize",
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_color(
        self, color: Color, start: int = None, end: int = None, background=True
    ) -> Type["Text"]:
        """Add color to the text.

        Args:
            color (Color): The color to be added.
            start (int, optional): The starting position of the text to apply the color to. Defaults to None.
            end (int, optional): The ending position of the text to apply the color to. Defaults to None.
            background (bool, optional): True if the color should be applied as the background color, False if it should be applied as the foreground color. Defaults to True.

        Returns:
            Type["Text"]: A new Text object with the added color.
        """
        background_type = "backgroundColor" if background else "foregroundColor"
        request = {
            "updateTextStyle": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "textStyle": {
                    background_type: color.as_color_request(),
                },
                "fields": background_type,
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_bold(self, start: int = None, end: int = None) -> Type["Text"]:
        """Add bold formatting to the text.

        Args:
            start (int, optional): The starting position of the text to apply the bold formatting to. Defaults to None.
            end (int, optional): The ending position of the text to apply the bold formatting to. Defaults to None.

        Returns:
            Type["Text"]: A new Text object with the added bold formatting.
        """
        request = {
            "updateTextStyle": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "textStyle": {
                    "bold": True,
                },
                "fields": "bold",
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_hyperlink(
        self,
        link: str,
        start: int = None,
        end: int = None,
        foreground_color: Color = None,
        underline=True,
    ) -> Type["Text"]:
        """Add a hyperlink to the text.

        Args:
            link (str): The URL for the hyperlink.
            start (int, optional): The starting position of the text to apply the hyperlink to. Defaults to None.
            end (int, optional): The ending position of the text to apply the hyperlink to. Defaults to None.
            foreground_color (Color, optional): The foreground color of the hyperlink. Defaults to None.
            underline (bool, optional): True if the hyperlink should be underlined, False otherwise. Defaults to True.

        Returns:
            Type["Text"]: A new Text object with the added hyperlink.
        """
        default_foreground_color = {"color": {"rgbColor": {"blue": 1.0}}}
        request = {
            "updateTextStyle": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "textStyle": {
                    "underline": underline,
                    "foregroundColor": foreground_color.as_color_request()
                    if foreground_color
                    else default_foreground_color,
                    "link": {"url": link},
                },
                "fields": "underline, foregroundColor, link",
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_heading(
        self, level: int, start: int = None, end: int = None
    ) -> Type["Text"]:
        """Add heading style to the text.

        Args:
            level (int): The level of the heading style.
            start (int, optional): The starting position of the text to apply the heading style to. Defaults to None.
            end (int, optional): The ending position of the text to apply the heading style to. Defaults to None.

        Returns:
            Type["Text"]: A new Text object with the added heading style.
        """
        heading = f"HEADING_{level}" if level > 0 else "NORMAL_TEXT"

        request = {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "paragraphStyle": {
                    "namedStyleType": heading,
                },
                "fields": "namedStyleType",
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    def add_list(self, level: int, start: int = None, end: int = None) -> Type["Text"]:
        """Add list formatting to the text.

        Args:
            level (int): The level of the list formatting.
            start (int, optional): The starting position of the text to apply the list formatting to. Defaults to None.
            end (int, optional): The ending position of the text to apply the list formatting to. Defaults to None.

        Returns:
            Type["Text"]: A new Text object with the added list formatting.
        """
        request = {
            "createParagraphBullets": {
                "range": {
                    "startIndex": start if start else self.position,
                    "endIndex": end if end else self._last_position,
                },
                "bulletPreset": "BULLET_STAR_CIRCLE_SQUARE",
            }
        }

        return Text(
            position=self.position,
            requests=self._requests + [request],
            last_position=self._last_position,
        )

    @staticmethod
    def new_line(position: int):
        """Create a new line in the text.

        Args:
            position (int): The position at which the new line should be added.

        Returns:
            tuple: A tuple containing the request for a new line and the new position.
        """
        return Text(position).add_text("\n").requests, position + 1
