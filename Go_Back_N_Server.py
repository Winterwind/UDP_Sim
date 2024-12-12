import socket, time
from UDP_Constants import addr as loc_addr, port as loc_port, bit_error_prob, packet_loss_prob, simulate_error

def go_back_n_receiver() -> None:
    # Create a UDP socket
    udpsoc = socket.socket(type=socket.SOCK_DGRAM)
    udpsoc.bind((loc_addr, loc_port))
    
    expected_packet = 0

    while True:
        recv_data, recv_addr = udpsoc.recvfrom(1024)
        
        # Simulate packet loss
        if simulate_error(packet_loss_prob):
            print("Packet loss simulated for data packet")
            continue  # Skip ACK to simulate loss
        
        # Simulate bit error
        if simulate_error(bit_error_prob):
            print("Data packet received but marked as corrupted")
            continue  # Skip ACK to simulate error
        
        print(f"Received packet {expected_packet}")

        # Simulate RTT
        time.sleep(0.05)

        # Send ACK for the expected packet
        if recv_data.decode() is not None:
            if not simulate_error(packet_loss_prob):
                ack_message = str(expected_packet).encode()
                udpsoc.sendto(ack_message, recv_addr)
                print(f"ACK {expected_packet} sent")
            else:
                print("ACK lost")
            expected_packet += 1

if __name__ == '__main__':
    go_back_n_receiver()
