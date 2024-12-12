import socket, time
from UDP_Constants import addr as rem_addr, port as rem_port, bit_error_prob, packet_loss_prob, simulate_error

# Send 1000 packets, each of 1 KB
num_packets = 100
packet_size = 1024  # 1 KB

def stop_and_wait_sender() -> None:
    # Counts for each scenario
    bit_errors = 0
    packet_losses = 0
    timeouts = 0
    packets_sent = 0

    # Create a UDP socket
    udpsoc = socket.socket(type=socket.SOCK_DGRAM)
    udpsoc.settimeout(1)  # Set timeout for ACK reception

    packet_data = b'X' * packet_size
    start_time = time.time()
    
    for packet_num in range(num_packets):
        while True:
            # Simulate packet loss
            if not simulate_error(packet_loss_prob):
                # Send the packet
                udpsoc.sendto(packet_data, (rem_addr, rem_port))
                packets_sent += 1
                print(f"Sent packet {packet_num}")
            else:
                packet_losses += 1
                print(f"Packet {packet_num} lost")

            try:
                ack, _ = udpsoc.recvfrom(1024)
                
                # Simulate ACK bit error
                if simulate_error(bit_error_prob):
                    bit_errors += 1
                    print(f"ACK for packet {packet_num} corrupted")
                    continue
                
                print(f"Received ACK for packet {packet_num}")
                break  # Exit loop on successful ACK

            # Catch timeout
            except socket.timeout:
                timeouts += 1
                print(f"Timeout, resending packet {packet_num}")

    total_time = time.time() - start_time
    print(f"Total transfer time: {total_time} seconds")
    print(f"{bit_errors} bit errors, {packet_losses} packet losses, {timeouts} timeouts, {packets_sent} total packets sent (including retransmissions), {packets_sent * packet_size} total bytes of data sent")
    print(f"Utilization rate: {total_time / (packets_sent * packet_size)}")

if __name__ == '__main__':
    stop_and_wait_sender()
