#!/usr/bin/env python3
"""
    filtered_logger.py
"""
import re
import os
import mysql.connector
from typing import List
import logging

PII_FIELDS: tuple() = ('email', 'phone', 'ssn', 'password', 'ip')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initializer function"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """output message in logging format"""
        # NotImplementedError
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter and obfuscate user PII"""
    for field in fields:
        message = replace(field, separator, redaction, message)
    return message


def replace(f: List[str], sep: str, red: str, m: str) -> str:
    """substitutes the matched pattern with the reduction"""
    pattern = f + '=.*?' + sep
    repl = f + '=' + red + sep
    return re.sub(pattern, repl, m)


def get_logger() -> logging.Logger:
    """return a logger object"""
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter())
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """return a database connector"""
    db: str = os.getenv('PERSONAL_DATA_DB_NAME')
    host: str = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    pwd: str = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    user: str = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    return mysql.connector.connect(user=user, password=pwd, host=host,
                                   database=db)
