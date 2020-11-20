
class Message():
    """
    Represent the structure of a CNS Message
    """

    def __init__(self) -> None:
        pass

    def encode(self):
        """
        Creates a byte-array which can be used to send data over a network channel.
        """
        pass

    @staticmethod
    def decode():
        """
        Creates a Message Object from a given byte-array received from the network
        """
        pass

    def add_header(self, header):
        """
        Add the Header for the Message
        """
        pass

    def add_queries(self, queries):
        """
        Add a list of queries to the Message
        """
        pass

    def add_answers(self, answers):
        """
        Add a list of answers to the Message Object
        """
        pass

    def resolve_queries(self, db):
        """
        Returns the Meesage Object which contains the answer for all the Queries in the Message from the database
        """
        pass
