import socket
from confundo_header import ConfundoHeader
from confundo.common import *  # Assuming common definitions used in client.py

def parse_flags(flags):
    flag_list = []
    if flags & FLAG_ACK:
        flag_list.append("ACK")
    if flags & FLAG_SYN:
        flag_list.append("SYN")
    if flags & FLAG_FIN:
        flag_list.append("FIN")
    return " ".join(flag_list)

def main():
    # Server configuration
    server_port = 5060  # You can change this to the port used in the client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', server_port))  # Replace '127.0.0.1' with the actual server IP
    
    print("Server is up and running ready to receive packets............. ")

    while True:
        data, addr = server_socket.recvfrom(MAX_UDP_PACKET_SIZE)
        header = ConfundoHeader.unpack(data[:ConfundoHeader.HEADER_SIZE])

        # Display the received packet information
        flags_str = parse_flags(header.flags)
        recv_info = f"RECV {header.sequence_number} {header.ack_number} {header.conn_id} {header.cwnd} {header.ss_thresh} {flags_str}"
        print(f"Packet received: {recv_info}")

        # Check if the packet is dropped due to an unknown connection ID
        if header.is_unknown_connection_id():
            dropped_info = header.packet_status()
            print(f"Packet dropped: {dropped_info}")
        
        # Send an ACK for the received packet back to the client
        ack_header = ConfundoHeader(header.ack_number, header.sequence_number + 1, header.conn_id, FLAG_ACK)
        ack_packet = ack_header.pack()
        server_socket.sendto(ack_packet, addr)

        # Display the information for the sent acknowledgment packet
        ack_flags_str = parse_flags(ack_header.flags)
        sent_ack_info = f"SEND {ack_header.sequence_number} {ack_header.ack_number} {ack_header.conn_id} {ack_header.cwnd} {ack_header.ss_thresh} {ack_flags_str}"
        print(f"Acknowledgment Sent: {sent_ack_info}")

if __name__ == "__main__":
    main()
