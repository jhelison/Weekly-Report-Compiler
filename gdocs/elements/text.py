from typing import Type
from gdocs.elements.util import Color


class Text:
    def __init__(self, position=0, requests=[], last_position=0):
        self._position = position
        self._requests = requests
        self._last_position = last_position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
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
        return self._last_position

    @property
    def requests(self):
        return self._requests

    def add_text(self, text) -> Type["Text"]:
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

    def add_hyperlink(
        self,
        link: str,
        start: int = None,
        end: int = None,
        foreground_color: Color = None,
        underline=True,
    ) -> Type["Text"]:
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
