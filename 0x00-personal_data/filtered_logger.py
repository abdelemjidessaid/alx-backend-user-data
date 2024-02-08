#!/usr/bin/env python3
"""
    Module of data logging
"""
from typing import List
import re
import logging
import os
import mysql
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function that returns the log message obfuscated"""
    return re.sub(r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)",
                  lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)


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
        """ function that returns the formated logs with obfuscated data"""
        formated = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, formated,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
        Function that returns a logger.Logger instance
    """
    user_data = logging.Logger('user_data', logging.INFO)
    user_data.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter.format(PII_FIELDS))
    user_data.addHandler(stream)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        Function that returns a MYSQL connector
    """
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    db_pass = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_pass,
        database=db_name
    )
    return connection
