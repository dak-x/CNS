use crate::*;
use std::collections::HashMap;
use std::{fs, str};
use toml::{self, Value};

lazy_static! {
    static ref FIELDS: Vec<String> = {
        let config_str =
            fs::read_to_string("./setup.toml").expect("Cound not Open config file at ./setup.toml");
        let config = config_str
            .parse::<Value>()
            .expect("Error reading setup file");
        let records = &config["database"]["records"];
        let mut fields = Vec::new();
        match records {
            Value::Array(records_arr) => {
                for field in records_arr {
                    fields.push(field.clone().to_string())
                }
            }
            _ => panic! {"Records List not found in config file: setup.toml"},
        }
        fields
    };
    static ref FIELDS_IDX: HashMap<String, u8> = {
        let mut _map = HashMap::new();
        let mut value: u8 = 64;
        for field in FIELDS.iter() {
            _map.insert(field.clone().into(), value);
            value = value / 2;
        }
        _map
    };
}

// ============= Message ==============
#[derive(Debug, Clone)]
pub struct Message {
    pub header: Header,
    pub queries: Vec<Query>,
    pub answers: Vec<Answer>,
}

impl CnsSend for Message {
    fn encode(&self) -> Vec<u8> {
        let mut encoded_stream: Vec<u8> = Vec::new();
        // Add header
        encoded_stream.append(&mut self.header.encode());
        // Join Queries
        if self.queries.len() > 0 {
            let encd_queries = self
                .queries
                .iter()
                .map(|x| {
                    let mut k = x.encode();
                    k.append(&mut "\n".to_string().into_bytes());
                    k
                })
                .flatten();
            // encoded_stream.append(&mut encd_queries);
            encoded_stream.extend(encd_queries);
        } else {
            // Join Answers
            let encd_answers = self.answers.iter().map(|x| x.encode()).flatten();
            encoded_stream.extend(encd_answers);
        }
        encoded_stream
    }
    fn decode(byte_stream: &mut [u8]) -> Self {
        let (header_stream, byte_stream) = byte_stream.split_at_mut(2);
        let header: Header = CnsSend::decode(header_stream);
        if (header.status / 4) % 2 == 1 {
            return Message {
                header,
                queries: Vec::new(),
                answers: Vec::new(),
            };
        }

        // Get queries if a query message
        let queries: Vec<Query> = {
            if header.status >= 8 {
                let mut queries: Vec<&mut [u8]> = byte_stream.split_mut(|&x| x == b'\n').collect();
                // remove "" from the last due to split
                queries.pop();

                queries.iter_mut().map(|x| CnsSend::decode(x)).collect()
            } else {
                Vec::new()
            }
        };

        let answers: Vec<Answer> = {
            if queries.is_empty() {
                let mut answers: Vec<&mut [u8]> = byte_stream.split_mut(|&x| x == b'\r').collect();
                // remove "" from the last due to split
                answers.pop();

                answers.iter_mut().map(|x| CnsSend::decode(x)).collect()
            } else {
                Vec::new()
            }
        };
        Message {
            header,
            queries,
            answers,
        }
    }
}

impl Message {
    pub fn new() -> Self {
        Message {
            header: Header::new(),
            queries: Vec::new(),
            answers: Vec::new(),
        }
    }

    /// Check is the message received is Well-Formed
    pub fn is_Ok(&self) -> bool {
        return (self.header.status / 4) % 2 == 0;
    }

    pub fn add_query(&mut self, query: Query) {
        self.queries.push(query);
    }
}

// ================ Header =================

#[derive(Debug, Clone)]
pub struct Header {
    pub id: u8,
    pub status: u8,
    pub nqueries: u8,
}

impl Header {
    fn new() -> Self {
        use rand::random;
        let id = random::<u8>();
        let status = 0;
        let nqueries = 0;
        Header {
            id,
            status,
            nqueries,
        }
    }
}

impl CnsSend for Header {
    fn encode(&self) -> Vec<u8> {
        vec![self.id, self.status * 16 + self.nqueries]
    }

    fn decode(byte_stream: &mut [u8]) -> Self {
        let id = byte_stream[0];
        let status = byte_stream[1] / 16;
        let nqueries = byte_stream[1] % 16;
        Header {
            id,
            status,
            nqueries,
        }
    }
}

// ================ QUERY ==================

#[derive(Debug, Clone)]
pub struct Query {
    pub which_fields: u8,
    pub name: String,
}

impl Query {
    pub fn make_query(name: String, field_list: Vec<String>) -> Self {
        let mut which_fields: u8 = 0;
        for field in field_list {
            which_fields += FIELDS_IDX.get(&field).unwrap_or(&0);
        }
        Query { which_fields, name }
    }
}

impl CnsSend for Query {
    fn encode(&self) -> Vec<u8> {
        let mut v = vec![self.which_fields];
        v.append(&mut self.name.clone().into_bytes());
        v
    }
    fn decode(byte_stream: &mut [u8]) -> Self {
        let which_fields = byte_stream[0];
        let name = str::from_utf8(&byte_stream[1..]).unwrap();

        Query {
            which_fields,
            name: name.to_owned(),
        }
    }
}

// ================ ANSWER ==================

#[derive(Debug, Clone)]
pub struct Answer {
    pub which_fields: u8,
    pub status_code: u8,
    pub records: Vec<String>,
}

impl Default for Answer {
    fn default() -> Self {
        Answer {
            which_fields: 0,
            status_code: 0,
            records: vec![],
        }
    }
}

impl CnsSend for Answer {
    fn encode(&self) -> Vec<u8> {
        let records_stream = (self.records.join("\n") + "\n\r").into_bytes();
        let mut encoded_answer = vec![self.status_code, self.which_fields];
        encoded_answer.extend(records_stream);

        encoded_answer
    }
    fn decode(byte_stream: &mut [u8]) -> Self {
        let status_code = byte_stream[0];
        let which_fields = byte_stream[1];
        let records_joined: &str = str::from_utf8(&byte_stream[2..]).unwrap();

        let mut records: Vec<String> = records_joined.split("\n").map(|x| x.to_owned()).collect();
        records.pop();
        Answer {
            status_code,
            which_fields,
            records,
        }
    }
}

#[test]
fn test_answer() {
    let mut orig = Answer::default();
    orig.records = vec!["Hello", "Its", "Me"]
        .iter()
        .map(|&x| x.into())
        .collect();

    let mut enc = orig.encode();
    let val_decoded: Answer = CnsSend::decode(enc.as_mut_slice());
    assert_eq!(format!("{:?}", orig), format!("{:?}", val_decoded))
}
#[test]
fn test_query() {
    let orig = Query {
        which_fields: 102,
        name: "TestName 12".to_owned(),
    };
    let mut enc = orig.encode();
    let val_decoded: Query = CnsSend::decode(enc.as_mut_slice());

    assert_eq!(format!("{:?}", orig), format!("{:?}", val_decoded))
}
#[test]
fn test_header() {
    let orig = Header {
        id: 10,
        status: 8,
        nqueries: 6,
    };
    let mut enc = orig.encode();
    let val_decoded: Header = CnsSend::decode(enc.as_mut_slice());
    assert_eq!(format!("{:?}", orig), format!("{:?}", val_decoded))
}

#[test]
fn test_message_query() {
    let header = Header {
        id: 10,
        status: 8,
        nqueries: 6,
    };
    let query = Query {
        which_fields: 102,
        name: "TestName 12".to_owned(),
    };
    let mut orig = Message::new();
    orig.header = header;
    orig.add_query(query);

    let mut encd_msg = orig.encode();
    let val_decoded: Message = CnsSend::decode(&mut encd_msg);
    assert_eq!(format!("{:?}", orig), format!("{:?}", val_decoded))
}
#[test]
fn test_message_answer() {
    let header = Header {
        id: 10,
        status: 0,
        nqueries: 6,
    };

    let mut orig = Message::new();
    orig.header = header;

    let mut answer = Answer::default();
    answer.records = vec!["Hello", "Its", "Me"]
        .iter()
        .map(|&x| x.into())
        .collect();
    orig.answers.push(answer);

    let mut encd_msg = orig.encode();
    let val_decoded: Message = CnsSend::decode(&mut encd_msg);

    assert_eq!(format!("{:?}", orig), format!("{:?}", val_decoded))
}
