import sys

def error_msg_details(error, error_detail:sys):
    _ ,_ , exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured python script name[{filename}] on line number [{exc_tb.tb_lineno}] and error msg is [{str(error)}]"
    return error_message

class SystemError(Exception):
    def __init__(self, error, error_detail:sys):
        super().__init__()
        self.error_message = error_msg_details(error, error_detail = error_detail)
    
    def __str__(self):
        return self.error_message