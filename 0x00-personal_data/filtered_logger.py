#!/usr/bin/env python3
"""filtered_logger."""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the logs message obfuscated.

    Args:
        fields (List(str)): a list of strings representing all fields
                             to obfuscate
        redaction (str): a string representing by what the field will
                          be obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character is
                          separating all fields in the log line (message)

    Returns (str): The logs message obfuscated.
    """

    return re.sub(
        fr"({'|'.join(map(re.escape, fields))})=[^ {re.escape(separator)}]*",
        f"\\1={redaction}", message)
