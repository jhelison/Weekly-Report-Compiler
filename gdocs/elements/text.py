class Text:
    def requests(self, position: int) -> list:
        pass

    def len(self) -> int:
        pass


class SimpleText(Text):
    def __init__(self, text: str):
        self.text = text

    def requests(self, position: int) -> list:
        requests = []

        requests.append(
            {
                "insertText": {
                    "location": {"index": position},
                    "text": self.text,
                }
            }
        )

        return requests

    def len(self) -> int:
        return len(self.text)


class TableHeaderText(Text):
    def __init__(self, text: str):
        self.text = text

    def requests(self, position: int) -> list:
        requests = []

        requests.append(
            {
                "insertText": {
                    "location": {"index": position},
                    "text": self.text,
                }
            }
        )

        requests.append(
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": position,
                        "endIndex": position + len(self.text),
                    },
                    "textStyle": {
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    "red": 255 / 256,
                                    "green": 217 / 256,
                                    "blue": 61 / 256,
                                }
                            }
                        },
                    },
                    "fields": "foregroundColor",
                }
            }
        )

        return requests

    def len(self) -> int:
        return len(self.text)


class ChipText(Text):
    def __init__(self, text: str):
        self.text = text

    def requests(self, position: int) -> list:
        requests = []

        requests.append(
            {
                "insertText": {
                    "location": {"index": position},
                    "text": self.text,
                }
            }
        )

        requests.append(
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": position,
                        "endIndex": position + len(self.text),
                    },
                    "textStyle": {
                        "foregroundColor": {
                            "color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}
                        },
                        "backgroundColor": {
                            "color": {
                                "rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
                            }
                        },
                    },
                    "fields": "foregroundColor,backgroundColor, fontSize",
                }
            }
        )

        return requests

    def len(self) -> int:
        return len(self.text)


class TextWithLink(Text):
    def __init__(self, text: str, link: str, remaining_text: str):
        self.text = text
        self.link = link
        self.remaining_text = remaining_text

    def requests(self, position: int) -> list:
        final_text = self.final_text()

        requests = []

        requests.append(
            {
                "insertText": {
                    "location": {"index": position},
                    "text": final_text,
                }
            }
        )

        # Add link styling
        requests.append(
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": position,
                        "endIndex": position + len(self.text),
                    },
                    "textStyle": {
                        "underline": True,
                        "foregroundColor": {"color": {"rgbColor": {"blue": 1.0}}},
                    },
                    "fields": "foregroundColor,underline",
                }
            }
        )

        # Add the hyperlink to the text
        requests.append(
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": position,
                        "endIndex": position + len(self.text),
                    },
                    "textStyle": {"link": {"url": self.link}},
                    "fields": "link",
                }
            }
        )

        return requests

    def len(self) -> int:
        return len(self.final_text())

    def final_text(self) -> str:
        return self.text + self.remaining_text
