from DB import DB
import toml
from CNS.Answer import Answer
from copy import copy

FIELDS = toml.load("setup.toml")["database"]["records"]
FIELDS_IDX = {}
val = 64
for x in FIELDS:
    FIELDS_IDX[x] = val
    val = val // 2

assert(len(FIELDS) < 8)


class Query():
    """
    Represents a Query Data Strcuture\n
    See Also: CNS-Message
    """

    def __init__(self) -> None:
        self.which_fields = 255
        self.name = "Test"

    def __repr__(self) -> str:
        return str(self.which_fields) + ": " + self.name

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
        return self.which_fields//128 == 1

    @staticmethod
    def make_query(name, fields):
        """
        Params: name - key , fields - Iterable:String \n
        Creates a Query Object which pertains to a query which request the fields of the key.
        """
        which_fields = 0
        # TODO: Raise error if field not found in config
        for field in fields:
            which_fields += FIELDS_IDX.get(field, 0)
        newQuery = Query()
        newQuery.which_fields = which_fields
        newQuery.name = name

        return newQuery

    def get_fields_list(self):
        """
        Returns a list of Fields to query in the DB
        """
        bin_string = bin(self.which_fields % 128)[2:].zfill(7)
        fields = []
        for indicator, field in zip(bin_string, FIELDS):
            if indicator == '1':
                fields.append(copy(field))

        return fields

    def resolve_query(self, db: DB) -> Answer:
        # Todo:
        """
        Params: db - database object\n
        Returns a Answer Object which is the result of the query.
        """
        answer_fields = db.fetch_fields(self.name, self.get_fields_list(),self.if_cache())
        if(answer_fields == -1):
            status_code = 0
            answer_fields = []
        else:
            status_code = 1

        newAnswer = Answer(answer_fields, status_code, self.which_fields)

        return newAnswer


# Test
if __name__ == "__main__":
    db = DB("data.json")
    temp = Query().make_query("Rob Marlo", ["Phone No.", "Email Personal"])
    # s = Query().encode()
    # print(Query())
    # print(int.from_bytes(s[:1], 'big'), s[1:].decode('utf-8'))
    # print(FIELDS_IDX)
    print(temp)
    print(temp.get_fields_list())
    print(temp.resolve_query(db))
    pass
