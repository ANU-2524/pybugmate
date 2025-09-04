from .color import c_info, c_error, c_return, c_profile

def log_info(message):
    print(c_info(message))

def log_return(message):
    print(c_return(message))

def log_error(message):
    print(c_error(message))

def log_profile(message):
    print(c_profile(message))
