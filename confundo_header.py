import struct
from confundo.common import FLAG_ACK, FLAG_SYN, FLAG_FIN


class ConfundoHeader:
    HEADER_FORMAT = '!I I H B'  # Define the format string for packing/unpacking the header

    # Calculate the header size based on the format string
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    def __init__(self, sequence_number, ack_number, conn_id, flags, cwnd=412, ss_thresh=12000):
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.conn_id = conn_id
        self.flags = flags
        self.cwnd = cwnd  # Congestion Window size attribute
        self.ss_thresh = ss_thresh  # Slow Start Threshold attribute

    def pack(self):
        return struct.pack(self.HEADER_FORMAT, self.sequence_number, self.ack_number, self.conn_id, self.flags)

    @classmethod
    def unpack(cls, packed_data):
        unpacked_data = struct.unpack(cls.HEADER_FORMAT, packed_data)
        return cls(*unpacked_data)

    def is_unknown_connection_id(self):
        # Check if the connection ID is unknown
        # Here you might implement a condition based on your logic for determining an unknown connection ID
        # For this example, we assume an unknown connection ID when it is zero
        return self.conn_id == 0

    def packet_status(self):
        if self.is_unknown_connection_id():
            return f"DROP {self.sequence_number} {self.ack_number} {self.conn_id} {self.get_flags()}"

    def get_flags(self):
        flag_list = []
        if self.flags & FLAG_ACK:
            flag_list.append("ACK")
        if self.flags & FLAG_SYN:
            flag_list.append("SYN")
        if self.flags & FLAG_FIN:
            flag_list.append("FIN")
        return " ".join(flag_list)
