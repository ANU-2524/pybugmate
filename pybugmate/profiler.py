from .color import c_info 

def profile_time(func , seconds) :
    print(c_info(f"[PROFILE] {func} ran for {seconds:.4f}s"))