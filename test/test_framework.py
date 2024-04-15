import functools
import traceback

class TestError(Exception):
    def __init__(self, message):
        self.message = message

def test(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
            print(f". PASSED: {fn.__name__}")
        except TestError as te:
            print(f"FAILED: {fn.__name__} - {te.message}")
        except:
            print(f"FAILED: {fn.__name__} - Uncaught exception occurred. Traceback: ")
            print(traceback.format_exc())
    return wrapper

def expect(left, right, on_fail):
    if left == right:
        return True
    else:
        raise TestError(on_fail)
