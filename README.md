# Host Discovery Service in SDN using Ryu Controller

##  Project Overview

This project implements a Host Discovery Service in a Software Defined Network (SDN) using the Ryu Controller. The system dynamically detects hosts connected to the network, maintains a host database, and installs flow rules to optimize packet forwarding.

The controller learns host details such as MAC address, IP address, switch ID, and port number in real-time using OpenFlow Packet-In messages.

---

##  Objectives

* Detect host join events dynamically
* Maintain a host database (MAC, IP, switch, port)
* Update host information in real-time
* Reduce controller overhead using flow rules
* Demonstrate controller-switch interaction in SDN

---

##  Technologies Used

* Python
* Ryu Controller
* Mininet Network Emulator
* OpenFlow Protocol (v1.3)
* Ubuntu 20.04 (VM)

---

##  System Architecture

The system consists of:

* **Ryu Controller**: Handles Packet-In events and installs flow rules
* **OpenFlow Switch (OVS)**: Forwards packets based on flow rules
* **Hosts (Mininet)**: Generate network traffic

Workflow:

1. Packet arrives at switch
2. Unknown packet sent to controller (Packet-In)
3. Controller extracts host details
4. Host database is updated
5. Flow rule installed in switch
6. Future packets handled directly by switch

---

##  Project Structure

```
sdn-host-discovery/
│
├── host_discovery.py
├── README.md
└── screenshots/
```

---

##  How to Run the Project

### Step 1: Start Ryu Controller

```
ryu-manager host_discovery.py
```

### Step 2: Start Mininet

```
sudo mn -c
sudo mn --topo single,3 --controller remote
```

### Step 3: Test Connectivity

```
pingall
```

---

##  Test Scenarios

###  Scenario 1: Normal Operation

* 3 hosts connected to switch
* All hosts communicate successfully
* Output: 0% packet loss

---

###  Scenario 2: Scalability

* Multiple hosts detected dynamically
* Host database updated automatically



---

###  Scenario 3: Failure Case

```
link s1 h1 down
pingall
```

* Link failure simulated
* Packet loss observed

---

##  Features

* Dynamic host detection
* Real-time host database maintenance
* IP learning using ARP and IPv4 packets
* Flow rule installation for efficient forwarding
* Reduced controller load after initial packets

---

##  Screenshots

### 🔹 Network Setup
<img width="851" height="483" alt="1_network_setup" src="https://github.com/user-attachments/assets/02c45bf6-9cc7-4da6-9178-baf0f60f2495" />


### 🔹 Ping Success
<img width="515" height="190" alt="2_ping_success" src="https://github.com/user-attachments/assets/42950c06-bb96-441e-b1e8-b7df91d9de08" />


### 🔹 Host Detection
<img width="1186" height="703" alt="3_host_detection" src="https://github.com/user-attachments/assets/51f70e15-11c1-4b4d-a463-0eb27a8822ad" />
<img width="1261" height="738" alt="3_host_detection_2" src="https://github.com/user-attachments/assets/6cdbd2e4-0826-4e5c-9194-2609e4a62bf5" />


### 🔹 Flow Table
<img width="1600" height="210" alt="4_flow_table" src="https://github.com/user-attachments/assets/90fae7fd-4183-4b6f-abfc-e0230a93d65f" />


### 🔹 Failure Case
<img width="519" height="221" alt="5_failure_case" src="https://github.com/user-attachments/assets/9417f77b-b399-49c3-a751-a6a04976efd6" />


---

##  Flow Table Verification

To verify flow rules installed in the switch:

```
ovs-ofctl dump-flows s1
```

This shows:

* Table-miss rule (priority 0)
* Installed flow rules (priority 1)

---

##  Learning Outcomes

* Understanding of Software Defined Networking (SDN)
* Controller-based network management
* OpenFlow protocol working (Packet-In, Flow-Mod)
* Traffic handling using flow rules
* Network programmability concepts

---

##  Conclusion

The project successfully demonstrates host discovery in an SDN environment using the Ryu controller. The system dynamically detects hosts, maintains a database, and optimizes traffic using flow rules, making the network efficient and programmable.
