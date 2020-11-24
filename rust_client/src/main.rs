use rust_client::*;
use std::collections::HashMap;
use std::net::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let requests: HashMap<u16, &str> = HashMap::new();
    let mut addr = SV_ADDR.to_string();
    addr.pop();
    let addr = format! {"{}:{}",&addr[1..],SV_PORT.to_string()};

    println! {"{}",addr};
    let mut sock = UdpSocket::bind("0.0.0.0:0")?;
    
    let msg = make_message(
        "Rob Marlo",
        &["Phone No.", "Email Personal", "Email Institute"],
    );

    
    println! {"{:?}\n\n",msg};
    let msg = msg.encode();
    let mut buf = [0; 1024];
    sock.send_to(msg.as_slice(), addr)?;

    let (bytes, _) = sock.recv_from(&mut buf)?;
    let mut buf = &mut buf[..bytes];

    let recv_message: Message = CnsSend::decode(buf);
    println! {"{:?}",recv_message};

    Ok(())
}

fn make_message(name: &str, fields: &[&str]) -> Message {
    let q = Query::make_query(name, fields);
    let mut msg = Message::new();
    msg.header.status = 8;
    msg.add_query(q);
    msg
}
