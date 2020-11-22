from DB import DB
from Answer import Answer
from Query import Query
from Header import Header


class Message():
    """
    Represent the structure of a CNS Message
    """

    def __init__(self) -> None:
        self.answers = []
        self.queries = []
        self.header = Header()

    def __repr__(self):

        queries = [repr(q) for q in self.queries]
        answers = [repr(a) for a in self.answers]

        return repr(self.header) + "\n" + " ".join(queries) + "\n".join(answers)

    def encode(self) -> bytes:
        """
        Creates a byte-array which can be used to send data over a network channel.
        """
        encoded_header = self.header.encode()
        encd_queries = [query.encode() for query in self.queries]
        encoded_queries = bytes(
            '\n', 'utf-8').join(encd_queries) + bytes('\n', 'utf-8')

        encd_answers = [answer.encode() for answer in self.answers]
        encoded_answers = b''.join(encd_answers)

        if(len(self.queries) > 0):
            return encoded_header + encoded_queries
        else:
            return encoded_header + encoded_answers

    @staticmethod
    def decode(byte_stream: bytes):
        # Todo: Add error handling for ill-formed requests
        """
        Creates a Message Object from a given byte-array received from the network
        """
        header_stream, rest = byte_stream[:2], byte_stream[2:]
        header = Header.decode(header_stream)
        message = Message()
        message.header = header

        # Query Message
        if(header.Status >= 8):
            # queries = list(map(Query.decode, rest.splitlines()))
            queries = [Query.decode(q) for q in rest.splitlines()]
            message.queries = queries
        # Answer Message
        else:
            answers = [Answer.decode(a) for a in rest.split(b'\r')[:-1]]
            message.answers = answers

        # How to distinguish between answer and query msg?
        return message

    def add_header(self, header):
        """
        Add the Header for the Message
        """
        self.header = header

    def add_queries(self, queries):
        """
        Add a list of queries to the Message
        """
        self.queries = queries
        self.header.Nqueries = len(queries)

    # No required right now
    def add_answers(self, answers):
        """
        Add a list of answers to the Message Object
        """
        self.answers = answers

    def resolve_queries(self, db: DB):
        """
        Returns the Meesage Object which contains the answer for all the Queries in the Message from the database
        """
        answers = [query.resolve_query(db) for query in self.queries]

        answer_message = Message()
        answer_message.header = self.get_header()
        answer_message.answers = answers

        return answer_message

    def get_header(self):
        """
        Returns the Header of the Message
        """
        return self.header


# tests
if __name__ == "__main__":
    db = DB("data.json")
    msg = Message()
    names = ["Rob Marlo", "Chenzi Dobi", "Bran Lopez"]
    fields = [["Section", "Email Institute"],
              ["Phone No.", "Section"],
              ["Email Personal", "Email Institute"]]

    queries = [Query.make_query(names[i], fields[i]) for i in range(3)]
    msg.add_queries(queries)
    print(msg)
    msg_response = msg.resolve_queries(db)
    print(msg_response)

    pass
