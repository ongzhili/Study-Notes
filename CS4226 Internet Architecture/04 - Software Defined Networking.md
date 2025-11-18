# Software Defined Networking

## Intro
### What is SDN?

- New approach to networking
    - Manage and implement network
- Traditional Approach of networking
    - Protocol defined approach
        - HTTP, TCP, UDP, etc

### Key to Internet's success

- Hourglass IP Model
- Layered Service Abstractions
    - Internet Protocol stack
    - Each layer can evolve independently
        - without changing other layers
- ONLY for network edges
    - they only have the upper layers (e.g TCP)


### Router / Switch at the core
- Recap
    - Router: Layer 3
        - Uses IP addresses
        - Crossing between multiple local networks
    - Switch: Layer 2
        - Uses MAC address
        - Find next hop
        - Local area network
- 2 key functions
    - Run routing algorithms / protocol (RIP, OSPF, BGP)
        - More software (algos to decide paths)
    - forwarding datagrams from incoming to outgoing link
        - More hardware (which port to use)

### Control Plane vs Data Plane

- **Control Plane**: Establish router state
    - Determine where to forward packet to
    - Relative slower
    - Generally has a broader view - neighbouring systems
- **Data Plane**: Process / Deliver packets
    - Actual deliver the packet
    - Much faster
    - Less broad view: Only see local information


## Design Principles
### Principle 1: Disaggregation

- Communication between data plane and control plane should be driven by open interfaces
    - Southbound interface

#### Implications
1. Network operators can purchase control and data planes from different vendors
    - Prevent vendor lock-in
2. Data plane consists of cheaper commodity forwarding devices (bare-metal switches)
    - Decoupling data plane with control plane
3. **Forwarding Abstraction** needs to be defined
    - Choose which vendor to buy the more expensive control plane hardware

#### Benefits

- Pros
    - New market landscape & value shift
        - Shift control from vendors to operators that build networks
    - Fast innovation
        - None of the 'Cisco is slow at implementing x feature' issue
        - Software can evolve independently of the hardware


### Principle 2: Centralized Control

"1 controller for the network"
- Switches on the data plane communicate to a single controller
    - In large enough use cases, controller can be a distributed system

#### Benefits

- Centralized Decisions are easier to make
    - Less complex as you have a global view of the system
    
- Logically centralized

#### Example of forwarding abstraction: OpenFlow

![alt text](image-10.png)

Flow rule: Match-Action pair

- Match and map to action
- Apply action

#### Where to implement the control plane?

1. Run software that implements control plane on-switch
    - Switches operate autonomously
        - Have to communicate with peer switches throughout the network to construct local routing tables
2. Make control plane physically decoupled from data plane
    - Control plane is implemented off-switch
        - e.g running in cloud
    - Possible to make it logically centralized

#### How to implement the data plane

- Option 1: fixed-function data plane
    - Header fields are well-known
    - Offsets are easy to compute
    - Match fields to actions (e.g OpenFlow)
- Option 2: programmable data plane
    - Data plane providing open interfaces about their internal structure
    - Instruct the data plane to identify certain part of the package header for a newly designed protocol

### Principle 3: Programmability



#### Benefits
- Easy network management
    - Management goals as policies
    - Easier to debug
- Control shift from vendor to users
    - Rapid innovation

### Summary: Design Principles

1. Separation of Control Plane and Data Plane (Disaggregation)
2. Logically Centralized Control (Centralization)
3. Programmability 

- Modularize the network control problem into the 3 layers of abstractions.
    - Specification
        - Allow a control application to express the desired network behavior without implementing it by itself
    - Distribution
        - Shield SDN apps from the distributed state, making distributed control logically centralized
    - Forwarding
        - Allow any forwarding behavior desired by apps while hiding details of underlying hardware

## Network Operating System

![alt text](image-11.png)

- Network OS itself is the control plane
    - OS provides high level abstractions to make it easier to write appplications
    - Network control functionality implemented by control apps

### Comparison with a traditional OS

![alt text](image-12.png)

- Southbound API in x86 / OpenFlow.
- "Data Plane" is x86 CPU / OpenFlow switch
- Northbound: Applications


### Abstractions

![alt text](image-13.png)

### Layers in a SDN

![alt text](image-14.png)

A more fine-grained implementation
- Note that control plane has a northbound interface, data plane has southbound interface

### Users of SDNs

1. Cloud providers
    - Google, MSFT, etc
2. Network operators (ISPs)
    - Comcast, AT&T, etc
3. Enterprises
    - Universities / Private companies

## Use Cases

### 1. Network Virtualization
- Existing virtualization solutions **(NOT NETWORK VIRTUALIZATION)**
    - VMs/ Containerization
    - VPNs / VLANs 
    - Limited scope: Virtualizing Address Space
- Need from mordern clouds
    - Create / Manage / Tear down networks **programatically**
        - Without manual configs
    - Disaggregation
        - Single API entry point to perform actions
    - Virtual network also has own private address space

![alt text](image-15.png)

- Virtual machines (can be on different hosts) still send and recieve packets through the underlying network
- **vS: Virtual Switch**
    - Behaves like a switch
    - Uses the physical NIC

### 2. Switching Fabrics

![alt text](image-16.png)

- Cloud datacenters
    - Lower costs
    - New Features

- **Leaf-spine topology**
    - **Spine Layer**
        - High capacity switches
        - Spine connects to all leaves
        - Spines do not connect to each other
    - **Leaf Layer** (Top-of-Rack (ToR)) switches - 1 per server rack
        - Each leaf connects to every spine
        - Servers connect only to leaf switches
    - This topology guarantees the following:
        - 2 hop Rack to Rack (multi-path)
            - Leaf -> Spine -> Leaf
            - Multi path allows for dynamic load balancing
        - 2 hop Intra-rack Server to Server
            - Server -> Leaf -> Server
        - 4 hop Inter-rack Server to Server
            - Server -> Leaf -> Spine -> Leaf -> Server

### 3. Traffic Engineering

- Optimizing how traffic flows through a network
    - For wide-area links between data centers (WANs: Wide-Area networks)
    - TE decides:
        - Which path to use
        - Bandwidth allocated
        - Which traffic gets priority
- Traffic classes with priorities
    - Delay tolerance vs availability

### 4. Software-Defined WANs

![alt text](image-17.png)

Allows MNCs to control everything from a centralized controller
- Apply network policies
- Topology + Performance
- Make routing decisions by:
    - Latency
    - Bandwidth
    - Priority
    - Geographical location (Some data might legally be required to be processed within a certain datacenter, etc)

### Summary

- Killer appications
    - Network virtualization
    - Datacenter / Cloud computing



## OpenFlow Protocol and Switch (SDN Protocols)

![alt text](image-18.png)

- Meter Table:
    - Counting / Metering packets from certain traffic flows
        - Primitive that we can configure programatically
        - Bandwidth allocation
- Group Table:
    - Aggregate multiple flows
        - Define a subset of ports = group
            - e.g Multicast Groups
    - Enable multiple actions

- Multiple controller controls a single switch?
    - Distributed System
    - Each controller takes a subset of switch
        - Synchronize with each other for a consistent global view
    - Conflict?
        - Not all the controllers communicate with the switch
        - Enables all the controller to be aware of all the switches in the network
        - Switches will run a leader election
            - 1 Main controller takes responsibility
                - Switch does the forwarding of information to all controllers to synchronize
                - Instead of the controller
                - Leader controller makes the actual change to the switch (when control plane needs to introduce new flow / entry / etc)

### OpenFlow pipeline

![alt text](image-19.png)

- 2 Main components
    - **Ingress** processing pipeline
    - **Egress** processing pipeline

- Allows us to apply logic based on separately:
    - Where the packet comes from
    - Where the package goes to

### OpenFlow terminology associated with packets

- Per packet from a packet flow:
    - Header + header field
    - Pipeline fields
        - "Variables associated with the pipeline"
        - Values attached to packet during pipeline processing
        - e.g ingress port, metadata
    - Action
        - Operation that acts on a packet
        - e.g drop, forward, modify (usually packet header only) (e.g decreasing TTL of pkt)
    - Action set
        - Multiple actions within an action set
        - Accumulated while processed at flow tables
        - Executed at the end of processing

### OpenFlow flow entry


- Flow entry in a flow table looks like this:
    - | Match Fields | Priority | Counters | Instructions | Timeouts |
        - Match fields: Packets are matched against
            - Header / Pipeline fields
            - May be wildcarded or bitmasked
            - A generalization of the longest prefix prefix matching of a traditional IP
        - Priority
            - Choose from multiple matches (higher priority first)
        - Instruction set
            - List of actions to apply immediately
            - Set of actions to add to the action set
            - Modify pipeline processing (Go to another flow table - only downstream)

- Contains a "default entry": Table-miss flow entry
    - Does not match an entry in the flow table
    - Typically send to control plane
        - Control plane installs table entry so that future packet matches can deal with it
    - Drop packet is also a potential action

#### OF Flow Entry: Macro
![alt text](image-20.png)

#### OF Flow Entry: Micro (Within each flow table)
![alt text](image-21.png)

### OpenFlow Switch in the typical network flow (Even more Macro)

![alt text](image-22.png)

1. Step 1: Sender sends packet (with source & dest ip addr, etc)
2. Step 2: SDN switch recieves packet. Attempt to match header with table flows
3. Step 3 & 4 (If no match: a.k.a first time seeing):
    - Step 3: Forward to control plane
    - Step 4: Control plane configues a new table entry (and installs it into flow table)
5. Packet gets forwarded to the target


## Interfaces of a SDN

- Eastbound and Westbound
    - Different SDN networks that want to communicate with each other / Or even to Legacy non-SDN networks
    - Instead of Northbound (SDN <-> Application) / Southbound (Control Plane <-> Data Plane)
    - No standard API yet
        - Northbound is not mature still, and is the current focus

## ONOS (Open Network Operating System) Control Plane 

- ONOS model
    - Open northbound API
    - Specification Abstraction
- ONOS system
    - Distribution abstraction

### NOS (Network Operating System)

- Can be thought of as a horizontally scalable cloud application
    - Contains loosely coupled subsystems
        - Each for 1 aspect of networking (e.g Topology, Host tracking)
        - Contains its own service abstraction
    - Similar to microservice architecture
    - Includes a scalable + highly available key/value store

### NOS Architecture

![alt text](image-23.png)

- Support multiple southbound APIs and multiple protocols (different adapters for different switches)
    - "Driver"

### Architecture of ONOS

- Northbound Interfaces (NBI)
    - Apps use it to stay informed about the network state
        - e.g Topology, Intercept Packets
- Distributed Core
    - Responsible for managing network state and notifying apps about relevant changes in state
    - Internal: Atomix (scalable key-value store)
- Southbound Interface (SBI)
    - Constructed from a set of plugins including shared protocol libs and device-specific drivers
    - Essentially allows us to communicate with the devices themselves

#### ONOS Abstractions

![alt text](image-24.png)

- Intent
    - high-level Intent
    - "What do you want, instead of how you want to operate the network"
        - Delegate this to the network to do the job
        - Network is ultimately responsible for how it is going to achieve that
- Flow Objective
    - Finer-grained control so that you can control the devices
    - Assume that these devices are logical
        - Does not include device-specific mechanisms
        - P4? OpenFlow? 
        - Delegate the action to the device
- Flow Rule
    - Even more devivce-specific
    - Used to control the various pipelines, fixed-function + programmable


## P4: Programming Protocol-independent Packet Processors

- Top-down design
- Make the data plane programmable

### P4: Introduction

- Domain-specific to formally define data plane pipeline
    - Protocol headers, lookup tables, etc
- As long as hardware supports P4, we can use it!

### Programmable Pipelines

![alt text](image-26.png)

- Protocol Independent Switch Architecture (PISA) reference model
- 3 main components
    - **Parser**
        - Process packet header
        - Extract all the needed packet header
        - Leave payload untouched (**only touches packet header**)
    - **Match-Action Pipeline**
        - Define tables
        - Define processing algorithm
            - Modify / Add / Remove headers, etc
    - **Deparser** (Serialized)
        - Reassemble the packet header back to the payload
            - Packet might look very different
        - "Inverse" operation of parser

### Logical to Physical
- P4 needs to account for different hardware vendors
    - Different chips implementing different physical pipelines
    - Important, as marketplace is not converged
        - Many different vendors with different NPU (Network Processing Unit)
        - Different vendors have different fixed-function components

- Solution: Vendor-specific logical pipelines
    - $P4_{16}$ (2016 P4) approach: A combination of:
        - Community-Developed:
            - Language
            - Core libraries
        - Vendor-supplied:
            - External libraries
            - Architecture definition

### P4: Terminology

#### P4 Architecture

- Definition
    - Abstraction that defines how packets flow through a pipeline
        - (Specifically, a programmable pipeline)
    - Describes the logical pipeline
        - General structure
        - Processing behavior
- Purpose
    - Standardize way to describe functionality of a P4-programmable device
    - Defines components and framework which a P4 program operates in

#### P4 Target

- Definition
    - Specific device / platform (Hardware / Software (e.g virtual switch))
    - The actual entity that processes the network packets
- Purpose
    - Concrete execution environment where a P4 program is deployed
- Characteristics
    - Has its own hardware capability
    - May have vendor-specific optimizations / constraints that can impact how P4 code is:
        - Mapped
        - Executed
        - e.g Compilation error when defined table is much larger than the hardware can accomodate