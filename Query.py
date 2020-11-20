import DB


class Query():
    """
    Represents a Query Data Strcuture\n
    See Also: CNS-Message
    """

    def __init__(self) -> None:
        self.which_fields = 255
        self.name = "\n"
        pass

    def encode(self):
        """
        Creates a byte-array which can be used to send data over a network channel.
        """
        name_stream = bytes(self.name, "utf-8")
        field_stream = self.which_fields.to_bytes(
            1, signed=False, byteorder="big")

        return field_stream + name_stream

    @staticmethod
    def decode(byte_stream: bytes):
        """
        Creates a Query Object from a given byte-array.
        """

        newQuery = Query()
        newQuery.name = byte_stream[1:].decode('utf-8')
        newQuery.which_fields = int.from_bytes(
            byte_stream[:1], byteorder='big')
        return newQuery

    def if_cache(self):
        """
        Checks whether query demands a Result only from the Cache of the DB
        """
        pass

    @staticmethod
    def make_query(name, fields):
        # Todo:
        """
        Params: name - key , fields - Iterable:String \n
        Creates a Query Object which pertains to a query which request the fields of the key.
        """
        newQuery = Query()
        newQuery.name = name
        newQuery.fields = fields

        return newQuery

    def resolve_query(self, db: DB):
        # Todo:
        """
        Params: db - database object
        Returns a Answer Object which is the result of the query.
        """

        pass


# Test
if __name__ == "__main__":
    s = Query().encode()
    print(int.from_bytes(s[:1], 'big'), s[1:].decode('utf-8'))
    pass
