from typing import Union, List


# Find a tag on the google docs document
# Returns the position and the tag_length
def find_tag(tag: str, content: list) -> Union[int, int]:
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
