from typing import ByteString


class Answer:

    def __init__(self, records, status_code):
        self.records = records
        self.status_code = status_code
        self.which_fields = 0   


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


# Tests
if __name__ == "__main__":
    pass