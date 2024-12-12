import random

# Set server details
addr = '127.0.0.1'
port = 50000

# Probability of bit error and packet loss
bit_error_prob = 0.1
packet_loss_prob = 0.1

def simulate_error(probability: int) -> bool:
    # Returns True if an event with the given probability should occur
    return random.random() < probability