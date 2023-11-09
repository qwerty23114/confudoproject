import sys
import socket
import os
import time
from confundo_header import ConfundoHeader
from confundo.common import *

def print_error_message(message):
    sys.stderr.write(f"ERROR: {message}\n")

def log_received_packet(header, is_ack=False):
    flags = ''
    if header.flags & FLAG_ACK:
        flags += " ACK"
    if header.flags & FLAG_SYN:
        flags += " SYN"
    if header.flags & FLAG_FIN:
        flags += " FIN"

    log_output = f"RECV {header.sequence_number} {header.ack_number} {header.conn_id}{flags}"
    if is_ack:
        log_output += " ACK"
    print(log_output)

def log_dropped_packet(header):
    flags = ''
    if header.flags & FLAG_ACK:
        flags += " ACK"
    if header.flags & FLAG_SYN:
        flags += " SYN"
    if header.flags & FLAG_FIN:
        flags += " FIN"

    log_output = f"DROP {header.sequence_number} {header.ack_number} {header.conn_id}{flags}"
    print(log_output)

def log_sent_packet(header, dup=False):
    flags = ''
    if header.flags & FLAG_ACK:
        flags += "ACK"
    if header.flags & FLAG_SYN:
        flags += " SYN"
    if header.flags & FLAG_FIN:
        flags += " FIN"
    if dup:
        flags += " DUP"

    log_output = f"SEND {header.sequence_number} {header.ack_number} {header.conn_id}{flags}\n"
    print(log_output)

def establish_connection(server_address, server_port, filename):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Initial values
    connection_id = 0
    sequence_number = INITIAL_SEQUENCE_NUMBER
    ack_number = 0
    packet_buffer = []

    cwnd = INITIAL_CWND_SIZE
    ssthresh = INITIAL_SS_THRESH
    last_acked = 0
    timeout = False
    last_ack_time = time.time()

    try:
        # Debug print statements to track the flow
        print("Connecting to the server...")

        server_info = (server_address, int(server_port))
        client_socket.settimeout(RETRANSMISSION_TIMEOUT)
        
        print("Attempting a 4-way Handshake...")

        # Send SYN packet to initiate connection
        print("Sending SYN packet...")

        syn_packet = ConfundoHeader(sequence_number, ack_number, connection_id, FLAG_SYN).pack()
        client_socket.sendto(syn_packet, server_info)

        # Receive SYN | ACK packet
        print("Waiting for SYN | ACK response...")

        syn_ack_packet, _ = client_socket.recvfrom(MAX_UDP_PACKET_SIZE)
        syn_ack_header = ConfundoHeader.unpack(syn_ack_packet[:ConfundoHeader.HEADER_SIZE])

        print("Received the SYN | ACK response...")

       
        print("Sending FIN packet...")
        fin_packet = ConfundoHeader(sequence_number, ack_number, connection_id, FLAG_FIN).pack()
        client_socket.sendto(fin_packet, server_info)


         # Expect an ACK for the FIN packet
        ack_for_fin, _ = client_socket.recvfrom(MAX_UDP_PACKET_SIZE)
        ack_for_fin_header = ConfundoHeader.unpack(ack_for_fin[:ConfundoHeader.HEADER_SIZE])

        if ack_for_fin_header.flags == FLAG_ACK:
            print("")

        else:
               print_error_message("Did not receive ACK for FIN packet")
               sys.exit(1)

        with open(filename, "rb") as file:
                while True:
                    data = file.read(MAX_PAYLOAD_SIZE)
                    if not data:
                        break

                    packet = ConfundoHeader(sequence_number, ack_number, connection_id, FLAG_ACK).pack() + data
                    packet_buffer.append((sequence_number, packet))

                    if len(packet_buffer) < cwnd // MAX_PAYLOAD_SIZE:
                        client_socket.sendto(packet, server_info)
                        sequence_number += len(data)

                    try:
                        received_packet, _ = client_socket.recvfrom(MAX_UDP_PACKET_SIZE)
                        received_header = ConfundoHeader.unpack(received_packet[:ConfundoHeader.HEADER_SIZE])

                        if received_header.flags == FLAG_ACK and received_header.sequence_number > last_acked:
                            last_acked = received_header.sequence_number
                            packet_buffer = [(seq, pkt) for seq, pkt in packet_buffer if seq > last_acked]

                            if cwnd < ssthresh:
                                cwnd += MAX_PAYLOAD_SIZE
                            else:
                                cwnd += (MAX_PAYLOAD_SIZE * MAX_PAYLOAD_SIZE) // cwnd

                            timeout = False
                            last_ack_time = time.time()

                    except socket.timeout:
                        timeout = True

                        if time.time() - last_ack_time > RETRANSMISSION_TIMEOUT:
                            ssthresh = cwnd // 2
                            cwnd = INITIAL_CWND_SIZE
                            timeout = False

                            for seq, pkt in packet_buffer:
                                if seq > last_acked:
                                    client_socket.sendto(pkt, server_info)
                                    sequence_number = seq + len(pkt) - ConfundoHeader.HEADER_SIZE

                    if timeout:
                        last_ack_time = time.time()


        if ack_for_fin_header.flags == FLAG_ACK:
                print("Received ACK for FIN packet")

                # Wait for incoming packets with FIN flag (FIN-WAIT)
                start_time = time.time()
                while time.time() - start_time < 2:
                    try:
                        packet, _ = client_socket.recvfrom(MAX_UDP_PACKET_SIZE)
                        packet_header = ConfundoHeader.unpack(packet[:ConfundoHeader.HEADER_SIZE])

                        if packet_header.flags == FLAG_FIN:
                            # Respond to each incoming FIN with an ACK packet
                            ack_packet = ConfundoHeader(packet_header.ack_number, packet_header.sequence_number + 1, connection_id, FLAG_ACK).pack()
                            client_socket.sendto(ack_packet, server_info)
                    except socket.timeout:
                        pass

                # Close the connection
                client_socket.close()
                print("4-way Handshake complete")
                print("Connection closed")
                sys.exit(0)
        else:
                print_error_message("Did not receive ACK for FIN packet")
                sys.exit(1)

    except socket.gaierror:
        print_error_message("Invalid hostname or port number")
        sys.exit(1)
    except FileNotFoundError:
        print_error_message("File not found")
        sys.exit(1)
    except Exception as e:
        print_error_message(str(e))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_error_message("Invalid number of arguments")
        sys.exit(1)

    hostname_or_ip, port, filename = sys.argv[1], sys.argv[2], sys.argv[3]
    establish_connection(hostname_or_ip, port, filename)
