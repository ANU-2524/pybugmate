import time
import functools
import sys
import traceback
from .logger import log_info, log_error, log_return, log_profile

def bugmate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log_info(f"[CALL] {func.__name__}({args}, {kwargs})")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            log_return(f"[RETURN] {repr(result)}")
            return result
        except Exception as e:
            log_error(f"[EXCEPTION] {type(e).__name__}: {e}")
            tb = traceback.format_exc()
            log_error(tb)
            tb_last = sys.exc_info()[2]
            if tb_last is not None:
                frame = tb_last.tb_frame
                for var, val in frame.f_locals.items():
                    log_error(f"    {var} = {repr(val)}")
            # raise
        finally:
            elapsed = time.time() - start
            log_profile(f"[PROFILE] {func.__name__} ran for {elapsed:.4f}s")
    return wrapper
