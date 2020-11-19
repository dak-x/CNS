# Project Division

- Protocol Design:
  - Port Number
  - Header Format
  - Message Format
   
- Server Implementation:
  - Make the server client in C++/python
  - Decide between DB or File
  - Record Structure
  
Header Structure: 
  - Id (16 bit)
  - which Records (8 bit) (using only 2 but can easily expand)
  - No of queries (1-16)
  - 


Record Strcture:
  - from a Config file (SQL)
  - and make the protocol generic over records

- Client Implementation:
  - Make libraries in atleast 3 languages
    - C++ 
    - Python 
    - Rust ( Daksh )
    - Java ( maybe )
  - Use these libraries to make examples


There is enough work to divide easily so no problem this time.