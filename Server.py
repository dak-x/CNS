import toml


class Server():
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


    def ignite(self):
        """
        Start the server
        """
        pass

    def __del__(self):
        """
        Destructor for the Server, Properly close connections with the db (if any)
        """
        pass

    def send_msg(self, message):
        """
        Sends a Message by encoding it a byte-stream and then sending over UDP
        """
        pass

    def recv_msg(self):
        """
        Listen the port for a Message Stream, and return that message
        """
        pass

# For testing purposes
if __name__ == "__main__":
    _ = Server("setup.toml")
