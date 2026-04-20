#!/usr/bin/env python3

import re
import subprocess
import sys
from urllib import parse
from .invoker import log_dataset_session_id, run, is_invoking_official_module

INVOKER_VERSION = '0.0.8'
COMMAND_OPTION_PATTERN = re.compile(r"^--(\w|-)+=.+", re.DOTALL | re.UNICODE)
EXTRA_DOUBLE_QUOTE_PATTERN = re.compile(r"^\"(.*\s.*?)(\\*)\"$", re.DOTALL | re.UNICODE)

def unescape_arg_value(value: str):
    """Reverse escape operations for command line arguments."""
    if re.match(EXTRA_DOUBLE_QUOTE_PATTERN, value):
        unquoted_value = value[1:-1]
        extra_end_backslash_count = (len(unquoted_value) - len(unquoted_value.rstrip('\\'))) // 2
        value = unquoted_value[:-extra_end_backslash_count] if extra_end_backslash_count > 0 else unquoted_value

    char_array = []
    backslash_seq_count = 0
    for ch in value:
        if ch == '\\':
            backslash_seq_count += 1
        else:
            backslash_seq_count = backslash_seq_count // 2 if ch == '"' else backslash_seq_count
            char_array.extend(backslash_seq_count * ['\\'])
            char_array.append(ch)
            backslash_seq_count = 0
    if backslash_seq_count > 0:
        char_array.extend(backslash_seq_count * ['\\'])
    return ''.join(char_array)

def unescape_arg(arg):
    if re.search(COMMAND_OPTION_PATTERN, arg):
        parts = arg.split("=", 1)
        return f'{parts[0]}={unescape_arg_value(parts[1])}'
    return arg

def decode(args):
    """URL decode and unescape all arguments."""
    return [unescape_arg(parse.unquote_plus(arg)) for arg in args]

def execute():
    """Main entry point for the urldecode invoker."""
    log_dataset_session_id()
    args = sys.argv[1:]
    print(f"Invoking module by urldecode_invoker {INVOKER_VERSION}.\n")

    decoded_args = decode(args)

    is_custom_module = not is_invoking_official_module(decoded_args)
    module_type = 'custom module' if is_custom_module else 'official module'
    print(f'Module type: {module_type}.\n')

    ret = run(decoded_args)
    sys.exit(ret)

if __name__ == '__main__':
    execute()
