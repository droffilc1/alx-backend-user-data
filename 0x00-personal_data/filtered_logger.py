#!/usr/bin/env python3
"""filtered_logger."""
from typing import List
import re
import logging
import os
import mysql.connector

# PII fields to be obfuscated
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format specified record as text.
        https://stackoverflow.com/questions/16757578/
        what-is-pythons-default-logging-formatter
        """
        return filter_datum(
            self.fields, self.REDACTION, super().format(record),
            self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """Creates a logger.
    Returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME ")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(user=user,
                                   password=password,
                                   host=host,
                                   database=database)
    return conn


def main() -> None:
    """Obtains a database connection using get_db and retrieve all rows
    in the users table and display each row under a filtered format.
    """
    #  Set up logging
    logger = get_logger()

    # Establish db connection
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [row[0] for row in cursor.description]

    for rows in cursor:
        msg = ''.join(f"{field}={str(row)};" for row,
                      field in zip(rows, fields))
        logger.info(msg.strip())

    # Close cursor and db connection
    cursor.close()
    db_conn.close()


if __name__ == '__main__':
    main()
