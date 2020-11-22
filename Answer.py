
class Answer:
    """
    Represents the Answer Structure conforming to the CNS Protocol
    """
    def __init__(self, records, status_code: int, which_fields: int):
        self.records = records
        self.status_code = status_code
        self.which_fields = which_fields

    def __repr__(self) -> str:
        if self.status_code == 0 :
            return "Status: Name not Found"
        else :
            return "Status: Ok" + "\nFields: " + str (bin(self.which_fields)[2:].zfill(8)) + ": "+ ", ".join(self.records)

    def encode(self) -> bytes:
        """
        Create a byte-array which can be used to send data over a network channel
        """
        records = "\n".join(self.records) + "\n\r"
        record_stream = bytes(records, 'utf-8')
        status_code_stream = self.status_code.to_bytes(
            1, byteorder='big', signed=False)
        which_fields_stream = self.which_fields.to_bytes(
            1, byteorder='big', signed=False)

        return status_code_stream + which_fields_stream + record_stream

    @staticmethod
    def decode(bytestring: bytes):
        """
        Create a Answer Object from  given
        byte-array
        """
        status_code = int.from_bytes(bytestring[:1], 'big', signed=False)
        which_fields = int.from_bytes(bytestring[1:2], 'big', signed=False)
        records = bytestring[2:].decode('utf-8').split("\n")
        records.pop() # removing \r split

        newAnswer = Answer("", 0, 0)
        newAnswer.status_code = status_code
        newAnswer.which_fields = which_fields
        newAnswer.records = records

        return newAnswer


# Tests
if __name__ == "__main__":
    s = Answer(["These", "are", "records"], 1, 240)
    print(s)
    # s_answer = Answer.decode(s.encode())
    # print(s_answer.status_code, ":", s_answer.which_fields)
    # print(s_answer.records)

