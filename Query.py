
class Query():
    """
    Represents a Query Data Strcuture
    See Also: CNS-Message

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
        Creates a Query Object from a given byte-array.
        """
        pass 

    @staticmethod
    def make_query(name,fields):
        """
        Params: name - key , fields - byte
        Creates a Query Object which pertains to a query which request the fields of the key.
        """
        pass   

    def resolve_query(self, db):
        """
        Params: db - database object
        Returns a Answer Object which is the result of the query.
        """
        pass

    