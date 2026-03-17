# 🧠 Brain to Brain Network (BBN) - Edge Processing Simulation
**Course:** CP352005 Networks | **Group:** 13
[cite_start]**Sprint 3 & 4:** Architecture Implementation & Validation [cite: 450, 467-470]

## 📌 Project Overview
[cite_start]The Brain-to-Brain Network (BBN) is a revolutionary conceptual framework designed to establish a direct, ultra-low-latency communication channel between human cortices, bypassing "The Bandwidth Bottleneck" of physical communication [cite: 496-498]. 

[cite_start]This repository contains the simulation code (`final_bbn_simulation.py`) and architectural documentation validating the **Neural Transport Protocol (NTP)** against standard TCP/IP[cite: 457, 500].

---

## 🔬 Sprint 3 & 4 Validation Results (The MVP)

Based on our SimPy simulation of 2,000 neural packets, we successfully optimized the network to meet strict biological constraints:

### 1. Ultra-Low Latency & Jitter (Layer 4)
* **Mathematical Formalization:** $L_{total} = L_{capture} + L_{NTP} + L_{decoding} \le 10ms$
* **Result:** NTP achieved an average latency of **~5.5 ms** with a Jitter of **< 1.0 ms**.
* [cite_start]**Impact:** `[PASS]` Successfully preserved Temporal Coding and completely avoided Motion Sickness warnings[cite: 619, 620]. Standard TCP/IP failed this constraint with an average of >18ms latency.

### 2. Edge-Processing Thermal Management (Layer 1)
* **Mathematical Formalization:** $\Delta T_{cortex} = \frac{P_{chip} \cdot t}{C_{tissue}} < 1.0^{\circ}C$
* [cite_start]**Result:** `[PASS]` Maximum tissue temperature remained under the critical **38.0°C** limit[cite: 523, 620].
* [cite_start]**Impact:** By converting Analog to Digital directly on the implanted chip with lightweight NTP frames, we prevented neuron death and scar tissue formation[cite: 520, 523, 541].

### 3. Neuro-Rights & Bio-Security (Session Layer)
* **Security Metric:** Malicious/Foreign Intent Drop Rate.
* **Result:** `[PASS]` The Bio-Security Filter successfully intercepted and blocked 100+ simulated malicious packets.
* [cite_start]**Impact:** Agency Protection is fully operational, preventing external hijacking of the user's motor cortex while enforcing the Human-in-the-Loop (HITL) mutual consent handshake [cite: 622, 780-781].

---

## 📊 Analytics & Visualizations
*(Note: Please find the generated output graphs in this repository)*
1. `latency_comparison.png`: Histogram proving NTP operates well below the 10ms threshold.
2. `thermal_load.png`: Line chart tracking heat dissipation stability.
3. `packet_loss_dist.png`: Pie chart comparing Neural packet delivery rates.

## 👥 Engineering Team
* **Architect:** Kantawit Naknuan (673380027-4)
* **Engineer:** Ratima Swasdi (673380055-9)
* **Network Specialist:** Thirawat Ujina (673380039-7)
* **DevOps:** Thanakrit Lakhonphon (673380269-0)
* **Tester/QA:** Kitiyada Kongkham (673380509-6)