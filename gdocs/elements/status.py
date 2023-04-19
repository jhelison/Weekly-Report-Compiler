from enum import Enum


class Status(Enum):
    # Dates tag
    TODO = "TO DO"
    WIP = "IN PROGRESS"
    HALTED = "HALTED"
    REVIEW = "REVIEW"
    DONE = "DONE"


def status_color(status: Status):
    if status == Status.TODO:
        return {
            "textStyle": {
                "foregroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 71 / 255,
                            "green": 56 / 255,
                            "blue": 33 / 255,
                        }
                    }
                },
                "backgroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 255 / 255,
                            "green": 229 / 255,
                            "blue": 160 / 255,
                        }
                    }
                },
            },
        }

    if status == Status.WIP:
        return {
            "textStyle": {
                "foregroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 12 / 255,
                            "green": 85 / 255,
                            "blue": 169 / 255,
                        }
                    }
                },
                "backgroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 191 / 255,
                            "green": 225 / 255,
                            "blue": 246 / 255,
                        }
                    }
                },
            },
        }

    if status == Status.REVIEW:
        return {
            "textStyle": {
                "foregroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 211 / 255,
                            "green": 211 / 255,
                            "blue": 211 / 255,
                        }
                    }
                },
                "backgroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 61 / 255,
                            "green": 61 / 255,
                            "blue": 61 / 255,
                        }
                    }
                },
            },
        }

    if status == Status.DONE:
        return {
            "textStyle": {
                "foregroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 38 / 255,
                            "green": 128 / 255,
                            "blue": 87 / 255,
                        }
                    }
                },
                "backgroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 212 / 255,
                            "green": 237 / 255,
                            "blue": 188 / 255,
                        }
                    }
                },
            },
        }

    return {
        "textStyle": {
            "foregroundColor": {
                "color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}
            },
            "backgroundColor": {
                "color": {"rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}}
            },
        },
    }
