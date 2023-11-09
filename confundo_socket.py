# File: confundo_socket.py

import socket
from confundo_header import ConfundoHeader

class ConfundoSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sequence_number = 0
        self.expected_sequence_number = 0
        self.is_connected = False
        self.window_size = 3  # Set the window size for sliding window
        self.buffer = []  # Buffer to store sent packets awaiting acknowledgment
        self.window_start = 0  # Index to track the start of the window
        # Other initialization logic
    
    def send(self, data, address, syn=False, fin=False):
        flags = 0
        if syn:
            flags |= 1  # Set SYN flag
        if fin:
            flags |= 4  # Set FIN flag
        
        header = ConfundoHeader(self.sequence_number, 0, 123, flags)
        packet = header.pack() + data
        
        if len(self.buffer) < self.window_size:
            self.socket.sendto(packet, address)
            if syn:
                response_data, _ = self.receive(buffer_size=1024)
                if response_data:
                    response_header = ConfundoHeader.unpack(response_data[:12])
                    if response_header.flags & 2:
                        self.is_connected = True
            self.buffer.append((self.sequence_number, packet))
            self.sequence_number += len(data)
        else:
            # Sliding window control: window full, wait for acknowledgments
            pass
    
    def receive(self, buffer_size):
        received_data, address = self.socket.recvfrom(buffer_size)
        header = ConfundoHeader.unpack(received_data[:12])
        data = None
        
        if header.flags & 1:
            ack_header = ConfundoHeader(0, header.sequence_number + 1, 123, 3)
            ack_packet = ack_header.pack()
            self.socket.sendto(ack_packet, address)
        
        if header.flags & 4:
            ack_header = ConfundoHeader(0, header.sequence_number + 1, 123, 5)
            ack_packet = ack_header.pack()
            self.socket.sendto(ack_packet, address)
            self.is_connected = False
        
        if not self.is_connected:
            data = received_data[12:]
        
        return data, address
    
    def close(self):
        if self.is_connected:
            self.send(b'', address=None, fin=True)
        self.socket.close()
        # Clean-up code
