import toml
import socket

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
        self.port = server_config.get("port")
        self.host = server_config.get("IP")
        self.buffer = server_config.get("buffer")

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
            d = self.recv_msg()
            self.send_msg("Recieved")

    def __del__(self):
        """
        Destructor for the Server, Properly close connections with the db (if any)
        """
        self.sock.close()
        pass

    def send_msg(self, message):
        """
        Sends a Message by encoding it a byte-stream and then sending over UDP
        """
        self.sock.sendto(str.encode(message), self.addr)

    def recv_msg(self):
        """
        Listen the port for a Message Stream, and return that message
        """
        self.data, self.addr = self.sock.recvfrom(self.buffer)
        print('debug', self.data)
        return self.data

    def resolveQuery(self, query):
        """
        Use functions of query to construct answer and return it
        """


# For testing purposes
if __name__ == "__main__":
    s = Server("setup.toml")
    s.ignite()
