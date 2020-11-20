
from typing import ByteString


class Answer:

    def __init__(self, records, status_code):
        self.records = records
        self.status_code = False
        self.which_records = 0   
        
    
    def get_answer(Name):
        pass 

    def fields(self):
        # Returns the 
        pass 

    
    def encode() -> bytearray:
        """
        Create a byte-array which can be used to send data over a network channel
        """
        pass 
    @staticmethod    
    def decode(bytestring: bytearray):
        """
        Create a Answer Object from  given
        byte-array
        """
        pass

