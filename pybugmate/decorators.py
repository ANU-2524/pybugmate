import time
import functools
import sys
import traceback
import inspect
from .logger import log_info, log_error, log_return, log_profile

def bugmate(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            log_info(f"[CALL] {func.__name__}({args}, {kwargs})")
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                log_return(f"[RETURN] {repr(result)}")
                return result
            except Exception as e:
                _log_exception_info(e)
                raise
            finally:
                elapsed = time.time() - start
                log_profile(f"[PROFILE] {func.__name__} ran for {elapsed:.4f}s")
        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log_info(f"[CALL] {func.__name__}({args}, {kwargs})")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            log_return(f"[RETURN] {repr(result)}")
            return result
        except Exception as e:
            _log_exception_info(e)
            raise
        finally:
            elapsed = time.time() - start
            log_profile(f"[PROFILE] {func.__name__} ran for {elapsed:.4f}s")
    return wrapper

def _log_exception_info(e):
    log_error("")
    log_error("🚨 [EXCEPTION] " + f"{type(e).__name__}: {e}")
    log_error("")
    tb = sys.exc_info()[2]
    last_frame = tb
    while last_frame.tb_next is not None:
        last_frame = last_frame.tb_next
    log_error("🔎 Locals at crash site:")
    for var, val in last_frame.tb_frame.f_locals.items():
        log_error(f"   {var} = {repr(val)}")

    # --- Some Hints 
    hints = {
        'ZeroDivisionError': "Hint: You tried to divide by zero. Ensure denominators are never zero.",
        'KeyError': "Hint: A required key was missing from a dict. Double-check your dictionary keys or use dict.get().",
        'TypeError': "Hint: You may have mixed types incorrectly (e.g., adding int and str). Check your variable types and function signatures.",
        'IndexError': "Hint: You tried to access an item beyond a list/array's limit. Check list length or for off-by-one errors.",
        'AttributeError': "Hint: You're trying to use a method or attribute that doesn't exist for this object. Is your variable the right type?",
        'ImportError': "Hint: The module or package you're importing is not installed or has a typo. Check spelling or pip install it.",
        'ModuleNotFoundError': "Hint: Python can't find that module. Check if you need to install it or if the import path is correct.",
        'ValueError': "Hint: A function received the right type but an inappropriate value (e.g., out-of-range number, empty string).",
        'NameError': "Hint: A variable or function name was used before it was defined. Check spelling and code order.",
        'StopIteration': "Hint: You called next() on an exhausted iterator, e.g., in a for-loop or generator.",
        'AssertionError': "Hint: An assert statement failed. Read the condition and make sure it's actually true.",
        'FileNotFoundError': "Hint: File or directory doesn't exist at the given path. Check typos, file creation, or cwd.",
        'PermissionError': "Hint: You lack permissions to read/write this file/dir. Try changing permissions or running as admin/root.",
        'RuntimeError': "Hint: An error occurred not covered by other error types. Read the message carefully.",
        'MemoryError': "Hint: Your program ran out of memory! Try smaller data or optimize your algorithm.",
        'IndentationError': "Hint: Python needs code to be correctly indented. Check for spaces/tabs mismatch.",
        'TabError': "Hint: Mixing spaces and tabs! Use only spaces or only tabs for indentation.",
        'TimeoutError': "Hint: The operation took too long. Did you set a timeout value that's too low?",
        'RecursionError': "Hint: Your function called itself too many times. Is there a missing base case?",
        'NotImplementedError': "Hint: This part of the code isn't implemented yet, or needs to be overridden in a subclass.",
        'OSError': "Hint: A system-level error occurred—file, process, or device related. See the error message for detail.",
        'IOError': "Hint: A problem with input/output (disk, file, network). Check file existence, permissions, or hardware.",
        'EOFError': "Hint: End of file reached unexpectedly (e.g., not enough input when reading).",
        'FloatingPointError': "Hint: Numeric error in floating point calculation (e.g., overflow, division by zero).",
        'ArithmeticError': "Hint: Numeric error (base class for ZeroDivisionError, OverflowError, etc).",
        'OverflowError': "Hint: Result of an arithmetic operation is too large for Python to handle.",
        'UnboundLocalError': "Hint: Variable referenced before assignment in local scope. Maybe assign it first?",
        'LookupError': "Hint: Invalid key, index, or search attempt—base class for IndexError and KeyError.",
        'BlockingIOError': "Hint: Non-blocking operation couldn't proceed immediately. Consider handling with select or try again.",
        'BrokenPipeError': "Hint: Communication channel was closed (e.g., writing to a closed pipe/socket).",
        'ConnectionError': "Hint: General connection error—subclass of OSError. Network/server may be unreachable.",
        'TimeoutError': "Hint: The operation took too long. Check timeout parameters or system/network load.",
        # Framework/library examples:
        'DjangoError': "Hint: Error from Django. Check settings.py, models, migrations, or template tags.",
        'FlaskException': "Hint: Error from Flask. Check route handlers, templates, or HTTP methods.",
        'TensorflowError': "Hint: TensorFlow-specific error. Check tensor shapes and layer inputs/outputs.",
        'PandasError': "Hint: Pandas-specific error. Check DataFrame/Series shapes and column names.",
        'NumpyError': "Hint: NumPy-specific error. Possible wrong shape, axis, or unsupported operation.",
        'ConnectionRefusedError': "Hint: Network connection refused. Is the server running/listening?",
        'ConnectionResetError': "Hint: Connection was forcibly closed by the remote host (SMTP, HTTP, etc).",
        # will add more later !!
    }

    hint = hints.get(type(e).__name__)
    if hint:
        log_error("💡 " + hint)
    log_error("")
    formatted_tb = ''.join(traceback.format_tb(last_frame))
    log_error("🔗 Code that crashed:")
    log_error(formatted_tb.strip())
    log_error("")  # Blank line !
