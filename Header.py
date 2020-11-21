import random


class Header():
    """
    Represents a CNS-Message header which is pre-pended on every request sent.
    """

    def __init__(self, nqueries):
        self.Id = random.randint(0, 255)
        self.Status = 4
        self.Nqueries = nqueries

    def __repr__(self) -> str:
        return "ID: " + str(self.Id) + "\n" + "Status: " + str(self.Status) + " Nqueries: " + str(self.Nqueries)

    def encode(self):
        """
        Creates a byte-array which can be used to send data over a network channel.
        """
        joined = self.Id * 256 + self.Status * 16 + self.Nqueries

        return joined.to_bytes(2, 'big', signed=False)

    @staticmethod
    def decode(bytestream: bytes):
        """
        Creates a Header Object from a given byte-array.
        """
        s = int.from_bytes(bytestream[:2], 'big', signed=False)

        newHeader = Header(0)
        newHeader.Id = s//256
        newHeader.Status = (s % 256)//16
        newHeader.Nqueries = s % 16

        return newHeader


# Test
if __name__ == "__main__":
    h = Header(12)
    h_encoded = h.encode()
    print(h_encoded)
    print(Header.decode(h_encoded))
