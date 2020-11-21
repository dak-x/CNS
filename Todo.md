Campus Name Server:
# Project Division:
- DB. Implementation
  - from_file()
  - fetch_key(Name)

- Python Implementation
  - Config File
  - Classes:
    - CNS-Server
    <!-- - CNS-Client -->
    - CNS-Message
    - Header
    - Query
    - Answer
  
  - CNS-Server:
    - run()
    - __init__(config)
    <!-- - send() -->
    <!-- - recv() -->
  - CNS-Message:
    - encode() -> byte String
    - decode()  byte String -> Message
    - build_query_msg()
    - build_answer_msg()
    - add_header()
    - get_header()
    - get_queries -> List(query)
    - get_answers -> List(answer)

  - Header:
    - init()
    - copy()
  
  - Query:
    - encode()
    - decode()
    - make_query()
    - resolve_query()
    - if_cache()

  - Answer:
    - encode()
    - decode()
    - Fields
    - get_answer(Name,Fields) -> Answer
    
# Project Desc.

- Protocol Design:
  - Port Number, Record Structure <- from **config file**.
  - Header Strcuture
  - Query & Answer Strcuture
   
- Header Structure: 
  - Id (8 bit)
  - Status (4 bit)
  - No of queries (1-16) (4 bits)
  - Copy from request to response
  
- Query Structure:
  - 1 Cache bit
  - which Records (7 bit) (using only 2 but can easily expand)
  - Name: String (variable size)
  - Terminated by \n
  
- Answer Structure:
  - Status Codes: 
    - Name not Found
    - Ok 
  - 1 Cache bit
  - which Records (7 bit) (using only 2 but can easily expand)
  - Each record terminated by \n
  - Each answer terminated by \r



# Think About it thorougly
- Record Structure:
  - Can have max of 7 fields
  - from a Config file (SQL)
  - and make the protocol generic over records

- Server Implementation:
  - Make the server client in C++/python
  - Decide between DB or File
  - Record Structure

- Client Implementation:
  - Make libraries in atleast 3 languages
    - C++ 
    - Python 
    - Rust ( Daksh )
    - Java ( Maybe )
  - Use these libraries to make examples

There is enough work to divide easily so no problem this time.