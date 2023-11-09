# confudoproject

# Project Name

## Team Members
- **Member 1 Name** (UID: XXXX)
  - Contribution: Describe the contributions and tasks completed by this team member.
- **Member 2 Name** (UID: XXXX)
  - Contribution: Describe the contributions and tasks completed by this team member.
- **Member 3 Name** (UID: XXXX)
  - Contribution: Describe the contributions and tasks completed by this team member.

## High-Level Design
### Server
The server architecture is built around a microservices design pattern. It comprises multiple components responsible for distinct tasks. These include:

Authentication Service: Manages user authentication and authorization.
Database Service: Handles database operations, ensuring data integrity and consistency.
Main Service: Acts as the core service, managing the primary functionalities of the application.
The server communicates using RESTful API endpoints, allowing seamless interaction between the client and the server. For the database, a relational database management system (e.g., PostgreSQL) was chosen for its robustness and scalability.

The communication between server and client is established via HTTP and WebSocket protocols. The HTTP protocol is used for general data exchange, while WebSocket ensures real-time bidirectional communication for specific features.

The server employs a modular design to ensure scalability and maintainability. This architecture enables easy integration of additional functionalities and ensures efficient handling of requests from multiple clients concurrently.

### Client

Certainly! Here's an explanation of the contents and functionalities of the client.py file:

Project Overview
The client.py file serves as the client-side script responsible for establishing a network connection with a server using the Confundo protocol. Its functionalities include managing packet exchanges between the client and server and implementing a reliable 4-way handshake protocol.

Functionalities
Error Handling and Logging

The script includes error messages via the print_error_message(message) function. It's designed to display error alerts on the standard error output.
Three logging functions are present:
log_received_packet(header, is_ack=False): Displays received packets' details and flags.
log_dropped_packet(header): Logs dropped packets, showcasing specific packet header details.
log_sent_packet(header, dup=False): Logs sent packets, exhibiting sequence numbers, acknowledgment numbers, connection IDs, and flags.
Connection Establishment

The establish_connection(server_address, server_port, filename) function acts as the primary driver. It's responsible for creating the connection.
It initiates a 4-way handshake by sending SYN packets to the server and awaits SYN | ACK responses.
It manages the timeout and retransmission mechanisms for ensuring reliable communication.
File Transfer and Closure

Once the handshake is established, the script handles file transfer through packets.
It sends ACK packets for received data, manages packet buffer for congestion control, and retransmits in case of timeout.
The script closes the connection by sending a FIN packet, awaits the corresponding FIN | ACK response, and closes the connection.
Execution Requirement

The script necessitates three arguments while execution:

python client.py <server_address> <server_port> <filename>

## Problems Encountered and Solutions
Problem 1: Socket binding failure

Description: The socket encountered an issue binding to a port due to an "Address already in use" error.
Solution: To resolve this problem, identify the process using the specified port and terminate it. Alternatively, you can change the port number or wait for the system to release the port.
Problem 2: Handshake failure during SYN packet exchange

Explanation: SYN packets weren't received by the server, causing a handshake failure.
Solution: Check the network connectivity between the client and server. Ensure the server is up and running. Verify firewall settings and ensure no packet loss during transmission.
## Additional Libraries Used
- List any external libraries utilized in the project and their purposes.

## Acknowledgements
Hunt, J. (2023). Sockets in python. In Advanced Guide to Python 3 Programming (pp. 557-569). Cham: Springer International Publishing.
Leon, J. F., Marone, P., Peyman, M., Li, Y., Calvet, L., Dehghanimohammadabadi, M., & Juan, A. A. (2022, December). A Tutorial On Combining FlexSim With Python For Developing Discrete-Event Simheuristics. In 2022 Winter Simulation Conference (WSC) (pp. 1386-1400). IEEE.

https://youtu.be/_FVvlJDQTxk

