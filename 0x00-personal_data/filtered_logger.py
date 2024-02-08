#!/usr/bin/env python3
"""
    Module of data logging
"""
from typing import List
import re
import logging
import os
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

    # Create a connection to the database and return it directly
    return mysql.connector.connect(
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.environ.get('PERSONAL_DATA_DB_NAME')
    )


def main():
    """
        Function that retrieve data from database and print it
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    result = cursor.fetchall()
    for row in result:
        message = 'name={}; email={}; phone={}; ssn={}; password={};'.format(
            row[0], row[1], row[2], row[3], row[4])
        print(message)
        log = logging.LogRecord(
            'my_logger', logging.INFO, None, None, message, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.format(log)
    cursor.close()
    db.close()


if __name__ == '__main__':
    """ Entry point of the Module """
    main()
