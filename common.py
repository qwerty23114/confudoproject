# File: confundo/common.py

# Maximum UDP packet size and payload size
MAX_UDP_PACKET_SIZE = 424
MAX_PAYLOAD_SIZE = 412

# MTU size for congestion control operations
MTU_SIZE = MAX_PAYLOAD_SIZE

# Maximum sequence and acknowledgment number
MAX_SEQUENCE_NUMBER = 50000
MAX_ACK_NUMBER = 50000

# Packet retransmission timeout
RETRANSMISSION_TIMEOUT = 0.5  # 0.5 seconds

# Initial and minimum congestion window size
INITIAL_CWND_SIZE = MAX_PAYLOAD_SIZE

# Initial slow-start threshold
INITIAL_SS_THRESH = 12000

# Initial sequence number
INITIAL_SEQUENCE_NUMBER = 50000

# FIN field takes one byte of the data stream
FIN_BYTE_SIZE = 1

# Constants for flags
FLAG_ACK = 0b100  # A (ACK, 1 bit)
FLAG_SYN = 0b010  # S (SYN, 1 bit)
FLAG_FIN = 0b001  # F (FIN, 1 bit)
