import functools
import traceback
from enum import Enum

class TestError(Exception):
    def __init__(self, message):
        self.message = message

class LogMessageType(Enum):
    SUCCEED = 1
    FAILED = 2
    INFO = 3

def log(message, type=LogMessageType.INFO):
    match type:
        case LogMessageType.SUCCEED:
            print("\033[1;32;40m SUCCESS: " + message)
        case LogMessageType.FAILED:
            print("\033[1;31;40m FAILED: " + message)
        case LogMessageType.INFO:
            print("\033[1;34;40m INFO: " + message)

def test(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            log(fn.__name__, LogMessageType.SUCCEED)
        except TestError as te:
            log(fn.__name__ + " - " + te.message, LogMessageType.FAILED)
        except:
            log(fn.__name__ + " - Uncaught exception occurred.", LogMessageType.FAILED)
            log(traceback.format_exc())
    return wrapper


def expect(bool_value, on_fail):
    if bool_value:
        return True
    else:
        raise TestError(on_fail)

def expect_not(bool_value, on_fail):
    if not bool_value:
        return True
    else:
        raise TestError(on_fail)


def expect_equal(left, right, on_fail):
    if left == right:
        return True
    else:
        raise TestError(on_fail)

def expect_not_equal(left, right, on_fail):
    if left != right:
        return True
    else:
        raise TestError(on_fail)

def expect_none(item, on_fail):
    if item is None:
        return True
    else:
        raise TestError(on_fail)
