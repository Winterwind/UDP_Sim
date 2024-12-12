import socket, time
from threading import Timer
from UDP_Constants import addr as rem_addr, port as rem_port, bit_error_prob, packet_loss_prob, simulate_error

# Configuration for Go-back-N
window_size = 7
num_packets = 100
packet_size = 1024  # 1 KB
timeout_interval = 1  # Timeout for retransmission

# State variables
base = 0  # First unacknowledged packet
next_seq_num = 0  # Next sequence number to be sent

# Timeout handler for retransmission
def retransmit_packets(udpsoc, packet_data) -> None:
    global base, next_seq_num
    for seq in range(base, next_seq_num):
        if not simulate_error(packet_loss_prob):
            udpsoc.sendto(packet_data[seq], (rem_addr, rem_port))
            print(f"Retransmitting packet {seq}")
        else:
            print(f"Packet {seq} lost during retransmission")

def go_back_n_sender() -> None:
    # Counts for each scenario
    bit_errors = 0
    packet_losses = 0
    timeouts = 0
    packets_sent = 0

    # Create a UDP socket
    global base, next_seq_num
    udpsoc = socket.socket(type=socket.SOCK_DGRAM)
    udpsoc.settimeout(timeout_interval)

    packet_data = [b'X' * packet_size for _ in range(num_packets)]
    timer = None
    start_time = time.time()

    while base < num_packets:
        # Send packets within the window
        while next_seq_num < base + window_size and next_seq_num < num_packets:
            if not simulate_error(packet_loss_prob):  # Simulate packet loss
                udpsoc.sendto(packet_data[next_seq_num], (rem_addr, rem_port))
                packets_sent += 1
                print(f"Sent packet {next_seq_num}")
            else:
                packet_losses += 1
                print(f"Packet {next_seq_num} lost")
            next_seq_num += 1

        # Start timer for the base packet if not already started
        if base < next_seq_num and timer is None:
            timer = Timer(timeout_interval, retransmit_packets, [udpsoc, packet_data])
            packets_sent += 1
            timer.start()

        try:
            ack, _ = udpsoc.recvfrom(1024)
            
            # Simulate ACK bit error
            if simulate_error(bit_error_prob):
                bit_errors += 1
                print(f"Corrupted ACK received, ignoring")
                continue

            ack_num = int(ack.decode())
            print(f"Received ACK for packet {ack_num}")

            # Slide the window
            if ack_num >= base:
                base = ack_num + 1
                if base == next_seq_num:
                    timer.cancel()  # All packets in the window are acknowledged
                    timer = None
                else:
                    timer = Timer(timeout_interval, retransmit_packets, [udpsoc, packet_data])
                    packets_sent += 1
                    timer.start()

        except socket.timeout:
            timeouts += 1
            print("Timeout, retransmitting unacknowledged packets")
            retransmit_packets(udpsoc, packet_data)
            packets_sent += 1

    total_time = time.time() - start_time
    print(f"Total transfer time: {total_time} seconds")
    print(f"{bit_errors} bit errors, {packet_losses} packet losses, {timeouts} timeouts, {packets_sent} total packets sent (including retransmissions), {packets_sent * packet_size} total bytes of data sent")
    print(f"Utilization rate: {total_time / (packets_sent * packet_size)}")

if __name__ == '__main__':
    go_back_n_sender()
