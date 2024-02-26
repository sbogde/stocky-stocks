# /backend/libs/misc/misc.py
from datetime import datetime


def get_formatted_timestamp(format_str="%Y%m%d-%H%M%S"):
    """Returns a formatted timestamp string."""
    return datetime.now().strftime(format_str)
