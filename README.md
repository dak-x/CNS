# CNS: Campus Name System Protocol
**CNS** is a <I>DNS</I> like system which is used to resolve names for an entity. The protocol is generic over the **Number** of records, but still has to put a limit on the maximum size. It is an Application level protocol, which works primarily over UDP, but it is still possible to run it over TCP. CNS supports asynchronous requests but this done via the client. The Server being over Udp cannot support async requests. All you require is our libraries to which offer an API to develop your own applications. 

## The Protocol:
Via the protocol all the exchanges include only a `CNS-Message` data structure which consists of a **Header** and Either a list of **Queries** or a a list of **Answers**. The client constructs the `Message` in accordance to a `setup.toml` file which is with both the server and client. The server return a Message with answer to the queries.

### CNS Message:
A CNS Message Consists of Two Strucutres
- A Header
- List of Queries/Answers 
    
#### CNS Header
A header has a constant size of 2 bytes: It has the following fields
- **Id**, a randomly generated 8-bit integer
- **Status Code**, a 4 bit integer
  - 1st Bit : Distinguishes between a **Query** or an **Answer** Message
  - 2nd Bit : Only used on a server response, signifies if the previous meesage received by the server is parsable or not. 
  - Rest: For future extension in the protocol  
- **Nqueries**, a 4 bit integer represents the number of Queries/Answers inside this Message. 

#### CNS Query
A `Message` can consists of a maximum of **16** queries.
A query consists of **two** fields
- **Which_Fields**, an **8** bit integer MSB specifies whether a client accepts cached results, and the last **7** bts specify which records to be fetched for a given **name**. This happens in compliance to the `setup.toml` file which configures the order of the records.
- **Name**, a String which is the key for the database records.

Each query is seperated by the `\n` character and a `Message` has a exactly **Nqueries** queries, which is specified in the `Header`.

#### CNS Answer
A `Message` can consists of a maximum of **16** answers. An answers consists of **three** fields
- **Status Code**, an **8** bit integer which has a value of **1** if the **name** was found, or **0** is it is not found.
- **Which_Fields**, an **8** bit integer MSB specifies whether the records were taken from the **Cache**, and the remaining **7** bit specify which fields this particular answer strcut contains
- **DB fields**, a list of fields asked in the corresponding query. Each fields is seperated by the `\n` character.

Each answers is seperated by the `\r` character and a `Message` has exactly **Nqueries** answers, which is specified in the `Answer`.

### Record Structure:  
All the record structure of the database is taken from a `setup.toml` file. It is assumed that both the server and client have the same `setup.toml` file. A possible extension for the protocol could be of performing a `handshake`, and exchange the `setup` files. But We have not made that the part of the protocol right now.


# Using this Client
## Python:
We have given a demo **Client-Server** implementation in this package. Our server and client share the `setup.toml` for the configuration. The records are stored in the `data.json` file. \
Run the server by running in terminal.

    python3 Server.py

Run the web-app by running in terminal.

    python3 app.py

Redirect to: [http://127.0.0.1:5000/] to use our client. \
The Python Package is located in the `CNS` directory. You can just copy this folder to your python project and use the `API` to develop your own application. Please refer to the files `Server.py` , `client.py` for an example use case.
## Rust:
We have provided only the `client` side functionalities in the `Rust Programming Language`.
The `src/lib.rs` file exposes all that you would require while writing a client in rust. Use the `src/main.rs` as an guide for using the API. \
You would still need a `setup.toml` file in the root directory of your rust project. \
Test the example client by running a server from the <I>**python**</I> implementation. And running from terminal. 

    cargo run -q




File any issues or bugs you found at this git repo, and request a PR if you want to contribute.

Authors:
- Daksh Chauhan
- Samarth Singh
- Pradyumn Sharma
- Aditya Naresh

