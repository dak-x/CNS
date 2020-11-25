import toml
import socket
from CNS import Message
from DB import DB
import logging

logging.basicConfig(filename="requests.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

class Server:
    """
    Represent a CNS Server Model which will do all that is necessary to run a Server Node for the CNS protocol.
    """

    def __init__(self, config) -> None:
        """ 
        params: config \n
        Instantiate a server with the config file and loads the database for the queries
        """
        # get the port from the config file
        conf = toml.load(config)
        server_config = conf.get("server")
        database_config = conf.get("database")
        self.port = server_config.get("port")
        self.host = server_config.get("IP")
        self.buffer = server_config.get("buffer")
        self.db = DB(database_config.get("path"))
        self.log = logging.getLogger()
        self.log.setLevel(0)

# Todo: Complete request processing
    def ignite(self):
        """
        Start the server
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print('debug', "Server Listening at port",
              self.port, "Addr", self.host)
        while(True):
            request = self.recv_msg()
            self.log.info(repr(request))
            self.resolveMessage()
            # self.send_msg("Recieved")

    def __del__(self):
        """
        Destructor for the Server, Properly close connections with the db (if any)
        """
        self.sock.close()
        pass

    def send_msg(self, message:Message):
        """
        Sends a Message by encoding it a byte-stream and then sending over UDP
        """
        self.sock.sendto(message.encode(), self.addr)

    def recv_msg(self):
        """
        Listen the port for a Message Stream, and return that message
        """
        data, self.addr = self.sock.recvfrom(self.buffer)
        self.msg = Message.decode(data)
        return self.msg

    def resolveMessage(self):
        """
        Use functions of query to construct answer and return it
        """
        if (not self.msg.is_Ok()):
            self.send_msg(self.msg)
        else:
            resolved_msg = self.msg.resolve_queries(self.db)
            self.send_msg(resolved_msg)



# For testing purposes
if __name__ == "__main__":
    s = Server("setup.toml")
    s.ignite()
