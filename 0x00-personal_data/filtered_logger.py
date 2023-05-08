#!/usr/bin/env python3
"""
    filtered_logger.py
"""
import re
from typing import List


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
