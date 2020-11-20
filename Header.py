import random


class Header():
    """
    Represents a CNS-Message header which is pre-pended on every request sent.
    """

    def __init__(self, nqueries: int):
        self.Id = random.randint(0, 255)
        self.Status = 0
        self.Nqueries = nqueries

    def encode(self):
        """
        Creates a byte-array which can be used to send data over a network channel.
        """
        pass 

    @staticmethod
    def decode():
        """
        Creates a Header Object from a given byte-array.
        """
        pass