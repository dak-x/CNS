use rust_client::*;
use std::net::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut addr = SV_ADDR.to_string();
    addr.pop();
    let addr = format! {"{}:{}",&addr[1..],SV_PORT.to_string()};

    println! {"{}",addr};
    let sock = UdpSocket::bind("0.0.0.0:0")?;
    
    let msg = make_message(
        "dqiku uwbkqj f",
        &["Phone No.", "Email Personal", "Email Institute"],
    );

    
    println! {"{:?}\n\n",msg};
    let msg = msg.encode();
    let mut buf = [0; 1024];
    sock.send_to(msg.as_slice(), addr)?;

    let (bytes, _) = sock.recv_from(&mut buf)?;
    let buf = &mut buf[..bytes];

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
