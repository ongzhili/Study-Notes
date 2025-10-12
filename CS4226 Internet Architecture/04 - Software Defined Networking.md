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

#### Example of forwarding abstraction: OpenFlow!

[alt text](image-10.png)