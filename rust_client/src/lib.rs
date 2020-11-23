use std::net;

/// A Trait which represents the encoding and decoding behaviour for the all the data types used in the CNS protocol
pub trait CnsSend {
    fn encode(&self) -> Vec<u8>;
    fn decode(byte_stream: &mut [u8]) -> Self;
}

// #[test]
// fn network_test() {
// use std::net::UdpSocket;
// let localhost = "127.0.0.1:27015";
// let mut sock =
// // UdpSocket::bind(localhost).expect("Couldn't open socket at" );
//
// // let buf = "Hello From this Side".to_string().into_bytes();
// // sock.send_to( &buf[..], "127.0.0.1:27013").unwrap();
// }
