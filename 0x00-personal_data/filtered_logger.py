#!/usr/bin/env python3
"""
    filtered_logger.py
"""
import re


def filter_datum(fields, redaction, message, separator):
    """filter and obfuscate user PII"""
    for field in fields:
        message = replace(field, separator, redaction, message)
    return message


def replace(f, sep, red, message):
    """substitutes the matched pattern with the reduction"""
    pattern = f + '=.*?' + sep
    repl = f + '=' + red + sep
    return re.sub(pattern, repl, message)
