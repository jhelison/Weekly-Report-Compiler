from gdocs.elements.text import Text
import re
from dataclasses import dataclass
from gdocs.elements.util import Status
from typing import List


LINKS_RE = r"\[([^\]]+)\]\(([^)]+)\)"
EMPHASIS_RE = r"`([^`]+)`"
BOLD_RE = r"\*\*([^*]+)\*\*"
HEADER_RE = r"^(#+)\s(.*)$"
LIST_RE = r"^(?<!\S)\s*-+\s+.+$"


@dataclass
class Match:
    text: Text
    position: int


class Markdown:
    def __init__(self, position: int, markdown: str):
        self.position = position
        self.markdown = markdown
        self._requests = []

    def process(self):
        lines = self.markdown.split("\n")

        for line in lines:
            line, matches = self.extract_tokens(line)
            if self._header(line, matches):
                pass
            elif self._list(line, matches):
                pass
            else:
                self._text(line, matches)

            self._new_line()
        return self._requests

    def _header(self, line: str, matches: List[Text]):
        match = re.match(HEADER_RE, line)

        if match is None:
            return False

        header_level = len(match.group(1))

        text = Text(self.position).add_text(match.group(2)).add_heading(header_level)
        self._requests.append(text.requests)
        self.position = text.last_position

        for match in matches:
            match.position = match.position - header_level - 1
            self._requests.append(match.requests)

        return True

    def _list(self, line: str, matches: List[Text]):
        match = re.match(LIST_RE, line)

        if match is None:
            return False
        
        # Replace the spaces with tabs
        line = "\t"+line
        replacements = 0
        parts = line.split("-", maxsplit=1)
        while "  " in parts[0]:
            parts[0] = parts[0].replace("  ", "\t")
            replacements += 1
        parts[1] = "● " + parts[1]
        line = "".join(parts)

        text = Text(self.position).add_text(line).add_heading(0)
        self._requests.append(text.requests)
        self.position = text.last_position

        for match in matches:
            match.position = match.position - replacements + 2
            self._requests.append(match.requests)

        return True

    def _text(self, line: str, matches: List[Text]):
        if line == "":
            line = " "

        text = Text(self.position).add_text(line).add_heading(0)
        self._requests.append(text.requests)
        self.position = text.last_position

        for match in matches:
            self._requests.append(match.requests)

    def extract_tokens(self, line: str):
        match = None
        matches = []

        while True:
            match = re.search(f"{LINKS_RE}|{EMPHASIS_RE}|{BOLD_RE}", line)
            if match is None:
                break

            # It's a link
            if match.group(2):
                matches.append(
                    Text(self.position).add_hyperlink(
                        link=match.group(2),
                        start=self.position + match.start(),
                        end=self.position + match.start() + len(match.group(1)),
                    )
                )
                text = match.group(1)

            elif match.group(0).startswith("`"):
                color = Status.NONE.status_to_color()
                text = match.group(0).replace("`", "")
                matches.append(
                    Text(self.position)
                    .add_color(
                        background=True,
                        color=color.background,
                        start=self.position + match.start(),
                        end=self.position + match.start() + len(text),
                    )
                    .add_color(
                        background=False,
                        color=color.foreground,
                        start=self.position + match.start(),
                        end=self.position + match.start() + len(text),
                    )
                )

            elif match.group(0).startswith("**"):
                text = match.group(0).replace("**", "")
                matches.append(
                    Text(self.position).add_bold(
                        start=self.position + match.start(),
                        end=self.position + match.start() + len(text),
                    )
                )

            else:
                break

            line = line[: match.start()] + text + line[match.end() :]

        return line, matches

    def _new_line(self):
        request, new_position = Text.new_line(self.position)
        self._requests.append(request)
        self.position = new_position


# Sample Markdown text
markdown_text = """
# My Favorite Movies

Here are some of my favorite movies:

- **The Shawshank Redemption**: This classic movie tells the story of two imprisoned men who form a strong bond over the course of many years.
    - **The Godfather**: This epic film follows the Corleone family as they navigate the world of organized crime.
        - **The Dark Knight**: Christopher Nolan's Batman movie is a masterclass in superhero filmmaking, with Heath Ledger delivering a legendary performance as the Joker.
- **The Princess Bride**: This charming fairy tale adventure has everything: romance, action, and plenty of laughs.

I highly recommend all of these movies to anyone who loves great storytelling and memorable characters.

"""

def clean_jira_markdown(markdown: str):
    # Remove <u> on links
    markdown = markdown.replace("</u>", "").replace("<u>", "")

    # Remove empty lines
    markdown = re.sub(r'\n{2}', '\n', markdown)
    markdown = re.sub(r'\n{2,}', '\n\n', markdown)

    return markdown