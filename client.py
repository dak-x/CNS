# Just for testing to be implemented as a class and to include config
import socket
import toml
from CNS import Message, Query


class Client:
    def __init__(self, config):
        conf = toml.load(config)
        server_config = conf.get("server")
        self.dest_addr = server_config.get("IP")
        self.dest_port = server_config.get("port")
        self.buffer = server_config.get("buffer")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.msg = Message()

    def send_qry(self):
        self.sock.sendto(self.msg.encode(), (self.dest_addr, self.dest_port))

    def make_qrymsg(self, qrylst, cacheFlag = True):
        queries = []
        for (name, field_list) in qrylst:
            q = Query.make_query(name, field_list,cacheFlag)
            queries.append(q)
        self.msg.add_queries(queries)

    def rcv_msg(self):
        return self.sock.recv(self.buffer)


# Test
if __name__ == "__main__":
    test_list = [["Rob Marlo", ["Section", "Email Institute"]], ["Chenzi Dobi", [
        "Phone No.", "Section"]], ["Bran Lopez", ["Email Personal", "Email Institute"]]]
    c = Client("setup.toml")
    c.make_qrymsg(test_list)
    c.send_qry()
    d = c.rcv_msg()
    d = Message.decode(d)
    for answer in d.answers:
        print(answer)
