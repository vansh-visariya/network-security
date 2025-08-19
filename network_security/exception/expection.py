import sys

class networkseacurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()  ## get the information for the error
        self.line_number = exc_tb.tb_frame.f_lineno  
        self.file_name = exc_tb.tb_frame.f_code.co_filename 

    def __str__(self):
        return "Error occured in file [{0}] at line number [{1}] error message [{2}]".format(
            self.file_name, self.line_number, str(self.error_message)
        )