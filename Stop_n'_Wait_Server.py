import socket, time
from UDP_Constants import addr as loc_addr, port as loc_port, bit_error_prob, packet_loss_prob, simulate_error

def stop_and_wait_receiver() -> None:
    # Create a UDP socket
    udpsoc = socket.socket(type=socket.SOCK_DGRAM)
    udpsoc.bind((loc_addr, loc_port))

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
        
        print("Packet received successfully")

        # Simulate RTT
        time.sleep(0.05)

        # Send ACK if no error or loss
        if not simulate_error(packet_loss_prob):
            ack_message = b'ACK'
            udpsoc.sendto(ack_message, recv_addr)
            print("ACK sent")
        else:
            print("ACK lost")

if __name__ == '__main__':
    stop_and_wait_receiver()
