# Just for testing to be implemented as a class and to include config
import socket
import toml
from Message import Message

class Client:
    def __init__(self,dest_addr, dest_port, config):
        conf = toml.load(config)
        server_config = conf.get("server")
        self.dest_addr = dest_addr
        self.dest_port = dest_port
        self.buffer = server_config.get("buffer")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send_qry(self, qry_msg):
        self.sock.sendto(qry_msg,(self.dest_addr, self.dest_port))

    def rcv_msg(self):
        return self.sock.recv(self.buffer)


# Test
if __name__ == "__main__":
    c = Client("127.0.0.1",27012,"setup.toml")
    c.send_qry(bytes('sa','utf-8'))
    d = c.rcv_msg()
    d = Message.decode(d)
    print(d)
    print(d.is_Ok())

