#!/usr/bin/env python3

import subprocess
import sys
import runpy
import logging
from contextlib import contextmanager

INVOKER_VERSION = '0.0.8'

def log_dataset_session_id():
    """Try printing the session id for better debugging Dataset issues."""
    try:
        from azureml._base_sdk_common import _ClientSessionId
        print('Session_id = ' + _ClientSessionId)
    except Exception:
        print('Session_id cannot be imported.')

@contextmanager
def run_without_logging_config():
    """Execute code without current logging config, then recover it."""
    original_handlers = logging.root.handlers
    logging.root.handlers = []
    try:
        yield
    finally:
        logging.root.handlers = original_handlers

def run_with_runpy(command):
    """Invoke module using runpy to avoid subprocess overhead."""
    with run_without_logging_config():
        module = command[2]
        print(f"Using runpy to invoke module '{module}'.\n")
        sys.argv = command[2:]
        runpy.run_module(module, init_globals=globals(), run_name='__main__')
        return 0

def run(command: list, timeout=60000):
    if not command:
        return
    # Check if it's a module invocation to use runpy
    if command[:2] == ['python', '-m']:
        return run_with_runpy(command)

    return subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr).wait(timeout=timeout)

def is_invoking_official_module(args):
    return len(args) >= 3 and args[0] == 'python' and args[1] == '-m' and args[2].startswith('azureml.studio.')

def execute():
    """Main entry point for the invoker."""
    log_dataset_session_id()
    args = sys.argv[1:]

    is_custom_module = not is_invoking_official_module(args)
    module_type = 'custom module' if is_custom_module else 'official module'
    print(f'Invoking {module_type} by invoker {INVOKER_VERSION}.')

    ret = run(args)
    sys.exit(ret)

if __name__ == '__main__':
    execute()
