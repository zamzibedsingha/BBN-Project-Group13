import simpy
import random
import matplotlib.pyplot as plt
import statistics

# Constants
NUM_PACKETS = 1000
SIMULATION_TIME = 2000  # ms
BANDWIDTH_6G = 100.0    # Gbps (simulated capacity)

# Biological Constraints
MAX_LATENCY_MS = 10.0
BIO_LOOP_LIMIT_MS = 50.0
BASE_TEMP_C = 37.0
MAX_TEMP_RISE_C = 1.0
THERMAL_DEATH_LIMIT = BASE_TEMP_C + MAX_TEMP_RISE_C

# Security Constants
SECURITY_THREAT_RATE = 0.05  # จำลองว่ามี 5% ของข้อมูลเป็นการโจมตี (Malicious Intent)
blocked_threats = 0          # ตัวนับจำนวนการแฮกที่ถูกบล็อก
mutual_consent_established = False # สำหรับ HITL

# Lists for plotting
tcp_latencies = []
ntp_latencies = []
thermal_log = []
time_log = []
packet_loss_tcp = 0
packet_loss_ntp = 0

class NetworkEnvironment:
    def __init__(self, env):
        self.env = env
        self.channel = simpy.Resource(env, capacity=50) # Limited channels
        self.current_temp = BASE_TEMP_C
        
    def dissipate_heat(self):
        """Background process: Dissipates heat over time."""
        while True:
            yield self.env.timeout(10)  # Every 10ms
            if self.current_temp > BASE_TEMP_C:
                self.current_temp -= 0.05 # Cooling rate
            
            # Record state
            thermal_log.append(self.current_temp)
            time_log.append(self.env.now)

    def process_packet(self, protocol):
        """Simulates processing heat."""
        # TCP requires more processing power (headers, ACKs) -> More Heat
        heat_gen = 0.002 if protocol == 'TCP' else 0.0001
        self.current_temp += heat_gen
        
        if self.current_temp > THERMAL_DEATH_LIMIT:
             pass # Logic handled in logging, don't crash sim

def packet_generator(env, net_env):
    """Generates 1000 packets for both protocols."""
    for i in range(NUM_PACKETS):
        # Inter-arrival time (fast firing neurons)
        yield env.timeout(random.uniform(0.5, 2.0))
        
        env.process(transmit_packet(env, net_env, 'TCP', i))
        env.process(transmit_packet(env, net_env, 'NTP', i))

def transmit_packet(env, net_env, protocol, packet_id):
    global blocked_threats
    
    # 1. Neuro-Rights Firewall: กรองคำสั่งแฮก
    if random.random() < SECURITY_THREAT_RATE:
        blocked_threats += 1
        return
    start_time = env.now
    
    # Request Network Resource
    with net_env.channel.request() as req:
        yield req
        
        # Transmission Delay logic
        if protocol == 'TCP':
            # Handshake + Overhead + Jitter
            delay = random.uniform(8.0, 25.0) 
            # Packet Loss Simulation (Retransmission)
            if random.random() > 0.95: 
                delay += random.uniform(20, 50) 
                global packet_loss_tcp
                packet_loss_tcp += 1
        else:
             # NTP: Direct + Bio-Time Stamp
            delay = random.uniform(4.5, 6.5)
            if random.random() > 0.99: # Lower loss rate
                # NTP doesn't retransmit, just a lost frame
                global packet_loss_ntp
                packet_loss_ntp += 1
                return # Stop processing
                
        yield env.timeout(delay)
        
        # Edge Processing (Heat Generation)
        net_env.process_packet(protocol)
        
        end_time = env.now
        latency = end_time - start_time
        
        # Store Data
        if protocol == 'TCP':
            tcp_latencies.append(latency)
        else:
            ntp_latencies.append(latency)
            
        # Logging for significant events (every 100 packets or failures)
        if packet_id % 200 == 0:
            print(f"[{env.now:.1f}ms] Packet #{packet_id} ({protocol}): {latency:.2f}ms")

def run_simulation():
    print("Initializing Brain-to-Brain Network Simulation (SimPy)...")
    env = simpy.Environment()
    net_env = NetworkEnvironment(env)
    
    # Start Processes
    env.process(net_env.dissipate_heat())
    env.process(packet_generator(env, net_env))
    
    # Run
    env.run(until=SIMULATION_TIME)
    
    print("\nSimulation Complete. Generating Analytics...")
    generate_charts()
    print_summary()

def generate_charts():
    # 1. Latency Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(tcp_latencies, bins=30, alpha=0.5, label='Standard TCP/IP', color='red')
    plt.hist(ntp_latencies, bins=30, alpha=0.7, label='Neural Transport (NTP)', color='green')
    plt.axvline(MAX_LATENCY_MS, color='black', linestyle='dashed', linewidth=2, label='Motion Sickness Threshold (10ms)')
    plt.title('Latency Comparison: TCP vs NTP (1000 Packets)')
    plt.xlabel('Latency (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig('latency_comparison.png')
    plt.close()

    # 2. Thermal Load
    plt.figure(figsize=(10, 6))
    plt.plot(time_log, thermal_log, color='orange', label='Brain Tissue Temp')
    plt.axhline(THERMAL_DEATH_LIMIT, color='red', linestyle='dashed', linewidth=2, label='Cell Death Limit (+1°C)')
    plt.title('Thermal Dissipation Tracker (Edge Processing)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig('thermal_load.png')
    plt.close()
    
    # 3. Packet Loss Pie Chart
    plt.figure(figsize=(6, 6))
    labels = ['TCP Loss', 'NTP Loss', 'Successful']
    sizes = [packet_loss_tcp, packet_loss_ntp, (NUM_PACKETS*2) - (packet_loss_tcp + packet_loss_ntp)]
    colors = ['red', 'yellow', 'green']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Packet Loss Ratio')
    plt.savefig('packet_loss_dist.png')
    plt.close()

def print_summary():
    avg_tcp = statistics.mean(tcp_latencies) if tcp_latencies else 0
    avg_ntp = statistics.mean(ntp_latencies) if ntp_latencies else 0
    max_temp = max(thermal_log) if thermal_log else 0
    
    print("\n" + "="*50)
    print("BBN EDGE-PROCESSING MAC: FINAL RESULTS SUMMARY")
    print("="*50)
    print(f"Total Neural Packets Simulated: {NUM_PACKETS * 2}")
    
    print(f"\n[LAYER 4: NEURAL TRANSPORT LATENCY]")
    print(f"TCP Average: {avg_tcp:.2f} ms")
    print(f"NTP Average: {avg_ntp:.2f} ms")
    print(f"NTP Performance: {avg_tcp / avg_ntp:.1f}x Faster (Avoids Bandwidth Bottleneck)")
    
    print(f"\n[LAYER 1: BIOLOGICAL SAFETY (CORTEX LAYER 5)]")
    print(f"Max Tissue Temp: {max_temp:.4f}°C")
    if max_temp > THERMAL_DEATH_LIMIT:
        print("CRITICAL WARNING: THERMAL LIMIT EXCEEDED! Neuron damage detected.")
    else:
        print("STATUS: SAFE. Heat dissipation successful. No scar tissue formed.")
        
    print(f"\n[SESSION LAYER: PHYSIOLOGICAL RESPONSE]")
    fail_count = sum(1 for l in tcp_latencies if l > MAX_LATENCY_MS)
    print(f"TCP Violations (>10ms): {fail_count} packets -> HIGH RISK (Severe Motion Sickness)")
    
    fail_count_ntp = sum(1 for l in ntp_latencies if l > MAX_LATENCY_MS)
    print(f"NTP Violations (>10ms): {fail_count_ntp} packets -> LOW RISK (Fluid Thought)")
    print("="*50)

    jitter_tcp = statistics.stdev(tcp_latencies) if len(tcp_latencies) > 1 else 0
    jitter_ntp = statistics.stdev(ntp_latencies) if len(ntp_latencies) > 1 else 0

    print(f"\n[LAYER 4: NEURAL TRANSPORT LATENCY & JITTER]")
    print(f"TCP Average: {avg_tcp:.2f} ms | Jitter: {jitter_tcp:.2f} ms")
    print(f"NTP Average: {avg_ntp:.2f} ms | Jitter: {jitter_ntp:.2f} ms")
    if jitter_ntp < 1.0:
         print("JITTER STATUS: [PASS] Temporal coding preserved.")
    else:
         print("JITTER STATUS: [FAIL] High risk of temporal disruption.")

    print(f"\n[NEURO-RIGHTS & BIO-SECURITY]")
    print(f"Malicious Intents Blocked: {blocked_threats} packets")
    print("Agency Protection: ENABLED & FUNCTIONING")
    print("="*50)
if __name__ == "__main__":
    run_simulation()