# Generate a formatted chips content for google docs
# Returns a list of dict with the change requests
def create_chip_request(text: str, text_size: int, location: int) -> list:
    return [
        {
            "insertText": {
                "location": {
                    "index": location,
                },
                "text": text,
            }
        },
        {
            "updateTextStyle": {
                "range": {
                    "startIndex": location,
                    "endIndex": location + len(text),
                },
                "textStyle": {
                    "foregroundColor": {
                        "color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}
                    },
                    "backgroundColor": {
                        "color": {"rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}}
                    },
                    "fontSize": {"magnitude": text_size, "unit": "PT"},
                },
                "fields": "foregroundColor,backgroundColor, fontSize",
            }
        },
    ]
