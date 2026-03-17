import time
import random

# Constants
DELAY_THRESHOLD_MS = 10.0
BIO_LOOP_LIMIT_MS = 50.0

def simulate_network_delay(protocol: str) -> float:
    """
    Simulates network transmission delay.
    
    TCP/IP Constraints:
    - Higher Protocol Overhead (Headers, ACKs)
    - Jitter from routing
    - Simulation range: 8ms to 25ms (often exceeding the 10ms limit)
    
    NTP (Neural Transport Protocol) Constraints:
    - UDP-like "Fire and Forget"
    - Bio-Time Stamping (Minimal overhead)
    - Direct Routing (Layer 3 optimized)
    - Simulation range: 2ms to 8ms (Targeting sub-10ms)
    """
    if protocol == 'TCP':
        # Simulating ACK overhead + standard jitter
        base_delay = random.uniform(8.0, 15.0) 
        # Occasional spike simulating packet loss/retransmission
        if random.random() > 0.8: 
            base_delay += random.uniform(10.0, 30.0)
        return base_delay
        
    elif protocol == 'NTP':
        # Simulating streamlined neural transport
        base_delay = random.uniform(2.0, 8.0)
        # Bio-Time Stamping ensures tight synchronization, very low jitter
        return base_delay

def run_simulation(num_packets=15):
    print(f"{'Packet':<8} | {'Protocol':<8} | {'1-Way Latency':<13} | {'Bio-Loop (RTT)':<15} | {'Result / Human Physiological Reaction'}")
    print("="*105)
    
    for i in range(1, num_packets + 1):
        # --- TCP/IP Simulation ---
        tcp_latency = simulate_network_delay('TCP')
        tcp_loop = tcp_latency * 2.1 # Simulate processing + return trip
        tcp_reaction = "[OK] Stable"
        
        if tcp_latency > DELAY_THRESHOLD_MS:
            tcp_reaction = "[!] MOTION SICKNESS TRACKED"
        if tcp_loop > BIO_LOOP_LIMIT_MS:
             tcp_reaction = "[!] SYNC BROKEN (Loop > 50ms)"
        if tcp_latency > 30.0:
            tcp_reaction = "[!!!] REJECTION (Neural Seizure Warning)"
            
        print(f"#{i:<7} | {'TCP':<8} | {tcp_latency:6.2f} ms     | {tcp_loop:6.2f} ms      | {tcp_reaction}")
        
        # --- NTP Simulation ---
        ntp_latency = simulate_network_delay('NTP')
        ntp_loop = ntp_latency * 2.05 # Faster processing with Bio-Time Stamp
        ntp_reaction = "[OK] Bio-Synced (Fluid Thought)"
        
        if ntp_loop > BIO_LOOP_LIMIT_MS:
            ntp_reaction = "[!] Feedback Loop Delayed"
        elif ntp_latency > DELAY_THRESHOLD_MS:
            ntp_reaction = "[!] Lag Spike (Minor Dizziness)"
            
        print(f"#{i:<7} | {'NTP':<8} | {ntp_latency:6.2f} ms     | {ntp_loop:6.2f} ms      | {ntp_reaction}")
        print("-" * 105)
        
        # Small sleep for dramatic effect in terminal
        time.sleep(0.3)

if __name__ == "__main__":
    print("\nStarting Brain-to-Brain Network (BBN) Protocol Simulation...")
    print(f"Constraints: Latency > {DELAY_THRESHOLD_MS}ms (Motion Sickness) | Bio-Loop > {BIO_LOOP_LIMIT_MS}ms (Sync Broken).")
    print("="*105)
    run_simulation()
    print("\nSimulation Complete.")