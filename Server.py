
class Server():
    """
    Represent a CNS Server Model which will do all that is necessary to run a Server Node for the CNS protocol
    """
    
    def __init__(self,config) -> None:
        """ 
        params: config 
        Instantiate a server with the config file and loads the database for the queries
        """
        pass 

    def ignite(self):
        """
        The Event loop for the Server
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