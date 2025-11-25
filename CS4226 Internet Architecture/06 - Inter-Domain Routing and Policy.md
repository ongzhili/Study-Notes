# Inter-Domain routing

- How ASes route / exchange traffic
    - **Intra-domain** routing protocol: within each AS
    - **Inter-domain** routing protocol: between AS

- Challenges:
    - Scale
    - Privacy
    - Policy

# Intra routing protocols

## 2 classes of routing algos (and why can't they work for inter-domain)

### 1. Link State
- All routes have complete topology
- All routes have link cost info
- Global or centralized
    - Based on Dijkstra's
    - Open Shortest Path First (OSPF)

#### Limitations
- Topology information is flooded
    - High bandwidth + storage overhead
    - Nodes divulge sensitive information (violates Privacy)

- Entire path computed locally per node
    - High processing overhead in large network

- Hard to find a universal metric
    - Different AS has different objectives
        - "Best route" for 1 might not be best route for another


### 2. Distance Vector Algorithm
- Route knows info of connected neighbors, link costs
- Decentralized Algorithm 
    - Based on Bellman-Ford Algorithm
    - Routing Information Protocol (RIP)

#### Better than 1?

- Hide details of network topology (no topology information flood)
- Only next hop determined by node

#### Limitations

- Slow convergence
    - RIP takes a long time to converge, especially when network is bigger (imagine the size of the internet)

- Still does not solve the universal metric / notion of total distance problem

# Path-Vector Routing: An extension to DV routing

![alt text](image-31.png)

- Solution: extend DV routing

- Key ideas: Advertise entire path
    - DV: send distance metric per destination *d*
    - PV: send entire path for each destination *d*

- Faster loop detection
    - Nodes can easily detect a loop
        - If node itself is in path = loop
            - Simply discard loop paths

# Protocol: Border Gatgeway Protocol (BGP)

- de facto inter-domain routing protocol
- runs between 2 routers

## BGP Operations

![alt text](image-32.png)
- BGP session
    - 2 BGP routers exchange messages
        - Advertise paths to different destination network prefixes
        - Runs through Layer 4 (Transport Layer) (TCP protocol)

## BGP / IGP model used in ISPs

- eBGP runs between ASes
    - exchange reachability information from neighbouring ASes
- iBGP runs within ASes
    - propagate reachability info across backbone
    - carry ISP's own customer prefixes
- IGP runs within ASes
    - Interior Gateway protocol


### eBGP: Exterior BGP Peering

- Runs between BGP speakers in different ASes
- Should be directly connected

- When AS1 advertises an IP prefix to AS2:
    - AS1 promises:
        - It will forward packets towards that prefix
        - AS can aggregate prefies in its advertisment (CIDR notation (`<ip>/<subnetmask>` e.g `192.168.1.0/24`))
            - Prefix matching possibility

### iBGP: Interior BGP Peering

- Peers within an AS
- Not required to be directly connected
    - IGP (RIP / OSPF) handles inter-BGP speaker connectivity
- iBGP peers must be (logically) fully meshed
    - iBGP speaker passes on prefixes learned from outside the AS
    - iBGP speaker **does not** pass on prefixes learned from other iBGP speakers
        - AS-PATH cannot prevent loops within a single AS, so the protocol blocks that behavior outright
        - A router that learns a prefix from outside via eBGP: propagate to rest
            - e.g A learns prefix from outside via eBGP: Propagate to B, C, D
            - But because iBGP is fully meshed, every router learns this information from A, no need to propagate

![alt text](image-33.png)

- Example here:
    - 1c recieves BGP messsage from 3a (**via eBGP**)
    - 1c distributes prefix info to all routers in AS1 (via **iBGP**)
    - 1b re-advertise info to AS2 over **eBGP**

### BGP messages

- OPEN
    - opens TCP connection to peer and authenticate sender
- UPDATE
    - advertises new paths (or withdraws old path)
- KEEPALIVE
    - keeps connection alive in absence of updates
    - also acts as an ACK for OPEN request
- NOTIFICATION
    - repors errors in previous messages
    - also used to close connection

### BGP messages: UPDATE message format

![alt text](image-34.png)

Key Observations:
- We can withdraw multiple routes in an update message
    - Specify length of withdrawn routes
- But we can only announce at most 1 new route per update message

- Network Layer Reachability Information (**NLRI**)
    - IP prefixes that can be reached from the advertised route


#### Withdrawn Routes

- No expiration timer for routes like RIP
- Invalid routes are actively withdrawn by original advertiser
    - Routes are considered available until explicitly withdrawn by announcing neighbour by:
        - Withdraw route
        - UPDATE message to replace existing route
        - Reduces amount of information exchange
- If a peer goes down, all routes from it become invalid
    - KEEPALIVE
        - No response -> assume router is down -> all routes invalid
    - NOTIFICATION
        - Connection closed -> all routes invalid

#### BGP Path Attributes
- 4 separate categories
    - well-known mandatory 
    - well-known discretionary (non mandatory)
    - optional transitive
    - optional non-transitive

- Each implementation of the BGP protocol needs to
    - Recognize all well-known attributes
    - Mandatory attributes MUST be included in UPDATE messages that contain NLRI
    - Once BGP peer updates well-known attributes, it must propagate to peers

##### Well-known mandatory attributes

- ORIGIN
    - Origin of the prefix, learned from:
        - `i` (IGP): Interior gateway protocol (RIP / OSPF) 
        - `?` (INCOMPLETE): Unknown source
        - `e` (EGP): Exterior gateway protocol (i.e BGP)
- AS-PATH
    - (It is a Path-Vector protocol after all)
    - Contains ASes through which NLRI has passed
    - Expressed as a sequence (e.g AS 78, AS 12) or a set
- NEXT-HOP
    - Indicates IP address of the router in the net-hop AS.
        - There might exist multiple links between any2 ASes
### Forwarding Table

![alt text](image-35.png)

- High level overview
    1. Router becoimes aware of IP prefix
    2. Router determines the output port for the IP prefix
    3. Router enteres the prefix-port pair in forwarding table

- BGP message contains "routes"
    - route = (destination) IP prefix + attributes: AS-PATH, NEXT-HOP
    - e.g route: `Prefix: 192.168.64.29/22; AS-PATH: AS3 AS131; NEXT-HOP: 201.44.13.125`
    - Router might recieve multiple routes for same destination prefix
        - Router has to select 1 route
            - Select best BGP route to prefix
                - Typically: Router selects route based on shortest AS-PATH
                    - e.g `AS2 AS18 AS98 to 130.16.64.29/22` vs `AS3 AS19 AS98 AS111 to 130.16.64.29/22`: Same destination prefix: select shortest route

            - What if there is a tie?
                - Typically: Best intra-domain routing cost (**Hot Potato Routing**)
                    - Choose route with closest NEXT-HOP
                    - Use selected route's NEXT-HOP
                        - IP addr of the router interface that begins the AS PATH
                        - e.g:![alt text](image-36.png)
                        - Router uses OSPF to find shortest path from 1c to `111.99.86.55`
                        - Router selects shortest OSPF path, adds prefix-port entry to the forwarding table: `192.168.64.29/2, port 4` (destination prefix, port to next-hop node with shortest path)

#### Forwarding Table: Summary

1. Router becomes aware of prefix
   * via BGP route advertisements from other routers

2. Determine router output port for prefix
   * choose the best inter-AS route from BGP
   * use OSPF to find best intra-AS route leading to best inter-AS route
   * identify port number for the best route

3. Enter prefix-port entry in forwarding table

### BGP Routing Information Bases

- A route in a BGP speaker is:
    - prefix + attributes = NLRI + Path Attributes

- All routes in a BGP speaker is:
    - Routing Information Bases (RIBs)
    - RIB is the sum of the following:
        - Adjacent RIBs In
            - Unprocessed routes from peers via an inbound UPDATE
            - Input for decision making
        - Local RIB
            - Selected local routes used by the router
        - Adjacent RIBs Out
            - Selected for advertisment to peers

### BGP Decision Process: Policy-based routing framework
![alt text](image-37.png)

- Each AS has its own freedom to implement the following, based on its own criteria
    - Apply Import Policies
        - Filter unwanted routes from neighbour
            - e.g Customer advertises a prefix that it does not own
        - Rank customer routes over peer routes
        - Manipulate attributes to influence path selection
            - e.g assign local preference to favoured routes
    - Apply Export Policies
        - Filter routes you don't want to tell your neighbour
            - e.g export only customer routes to peers & providers
                - Since they make money of traffic send to customers
        - Manipulate attributes to control what they see
            - e.g Artificially make paths look longer (AS prepending)
                - e.g `AS5 AS1 AS3 -> AS5 AS5 AS5 AS5 AS1 AS3`
    - Best Route Selection

#### BGP Policy: In practice

- Commercial ISP
    - Fulfill bilateral agreements with other ISPs
    - Minimize monetary cost / Maximize revenue
    - Ensure good performance for customers

- Bilateral agreement between neighbour ISPs
    - Defines who provides transit for what
    - Depends on business relationship

### Customer-Provider Relationship: Extension

![alt text](image-38.png)

1. Customer pays provider for access to internet
    - Provider exports customer's routes to everybody
        - Entire internet can reach customer
    - Customer export provier's routes to customers
        - Allows its own customers to use the upstream

### Peer-to-Peer relationship

![alt text](image-39.png)

1. Peers exchange traffic between customers
    - AS exports only customer routes to a peer
    - AS exports a peer's routes only to its customers
    - So that customers of 1 AS can transit traffic to customer of another AS through the peering link



### BGP Attributes: Continuation

- LOCAL_PREF
    - Influence **outbound** traffic
        - It is used to influence the preferred outbound path when multiple routes to the same destination prefix exist.
    - 4 byte unsigned integer (default value 100)
        - Higher = more priority
    - for BGP speaker to inform its other internal peers of its degree of preference for a specific route
    - Propagated **within** an autonomous system
        - Include in UPDATE messages that are sent to internal peers
        - Not included in UPDATE message sent to external peers
- MULTI_EXIT_DISC (MED)
    - Influence **inbound** traffic
        - "This path (MED) is longer (value is higher)"
        - Allows control of inbound traffic by directing traffic to lower MED values (potentially)
    - Used between two ASes when they have multiple connection points.
    - 4 byte unsigned integer (default value 0)
        - Lower = better
    - for BGP speaker to discriminate among multiple entry points to a neighbouring AS to control inbound traffic
    - Must not be propagated to neighbouring ASes

- COMMUNITY
    - 4 byte integer value 
    - Label
        - Used to group destination
    - Useful in applying policies within and between ASes
        - Apply policies based on COMMUNITY attribute


### BGP best route selection: Common practices
1. Calculation of degree of preference
    - If route is learned from an internal peer:
        - use LOCAL_PREF
    - Else:
        - use preconfigured policy

2. Route Selection (recommended)
    - Highest degree of LOCAL_PREF
    - If Tie / Not used, Smallest number of AS numbers in AS_PATH
    - If Tie / Not used, Lowest origin number in ORIGIN attribute
    - If Tie / Not used, Most preferred MULTI_EXIT_DISC attribute
    - If Tie / Not used, eBGP route > iBGP
    - If Tie / Not used, Lowest interior cost based on NEXT_HOP attribute

### Network Security: 

#### BGP Prefix Hijacking

![alt text](image-40.png)

- Orange: advertising a destination ip that it does not own
- Green: Original AS
- Some traffic can be directed to orange (impersonator)

#### BGP Subprefix Hijacking
![alt text](image-41.png)

- AS advertises a more specific IP prefix (/24 instead of /16)
    - Everyone will eventually send traffic to this impersonator
        - Due to longest prefix matching mechanism of IP
            - This subnet mask is more specific


#### Preventing (Sub)prefix Hijacking

- Best Common practice for route filtering
    - AS filters routes announced by customers
        - Based on prefixes the customer owns

- Industrial Trends
    - Routre Origin Authorisation (ROA)
    - Resource Public Key Infrastructure (RPKI) 


### BGP Summary: How it is used in practice

- Three classes of "knobs"
    - Preference
        - Add / Delete / Modify attributes
    - Filtering
        - Inbound / outbound filtering
    - Tagging
        - COMMUNITY attribute in BGP message

- Applications
    - Business relationships
        - Influence decision process (LOCAL_PREF)
        - Controlling route export (COMMUNITY)
    - Traffic engineering 
        - Inbound (MED / AS pre-pending)
        - Outbound (LOCAL_PREF, IGP cost)
        - Remote control (COMMUNITY)


## Peer-to-Peer networks


### Traditional communication model: Socket programming (Client-server model)

- Asymmetric
- Client initiates request, server provides response


### P2P network

![alt text](image-42.png)

#### Properties
- No always-on server or central entity
- Arbitrary end systems directly communicate
- Flat architecture / namespace
#### Problems
- Peers are intermittently connected
    - They come and go (join / leave)
    - Change IP addresses
- Unreliable service providers
- Staying connected is an issue
- Resource lookup?

### P2P Network Case study 1: Napster

![alt text](image-43.png)

- Based on a central index server
    - User registers with this server
    - Server sends a list of files to be shared
    - Server knows all the peers and files in network

- Search based on keywords
    - Results:
        - File Info + Peer that is sharing it

- Advantages
    - Consistent view of the network
    - Fast and efficient searching
    - Guarantee correct search answers
        - Peer has the file -> You can initiate download
- Disadvantages
    - SPoF (If central index server goes down, the entire network is not functional)
    - Large computation to handle queries (central server)
    - Only download from a single peer (search result only shows 1 peer per result)


### P2P network Case study 2: Gnutella
![alt text](image-44.png)

- Pure P2P network
    - Absence of central index server (of Napster)
    - Contains only peers

- How to join without a central server?
    - Peer needs the address of another active peer
        - Obtained from a out-of-band channel (e.g forum, other communication network)
    - New joiner learns about other peers and topology of network
        - Queries are flooded into the network
    - Download directly between peers

- Advantages
    - Fully distributed / Decentralized
        - Robust against random node failures
    - Open protocol
    - Less susceptible to DoS
- Disadvantages
    - Inefficient query flooding
        - Every time a new peer joins -> flood -> wastes a lot of network and peer resources
    - Inefficient network management
        - Constantly probe nodes

### P2P network Case study 3: KaZaA

![alt text](image-45.png)

- Two kinds of nodes in the network
    - Ordinary Nodes (ON): A normal peer user
        - Obtain address of SN -> Send request and gives list of file to share
        - SN starts keeping track of ON
    - Supernodes (SN): User peer with more resources / responsibilities than ON
        - Exchange information between themselves
            - Flooding between the Supernodes
            - More efficient that a Gnutella network as less resources wasted on flooding (even though it still floods)
        - Do not form a complete mesh
        -   Other SNs do not see ONs that do not connect to them
- Forms a two-tier hierarchy
    - Top: SN, Bottom: ON
    - ON can only belong to only one SN at any time
        - Can change at will
        - SN acts as a "hub" for all ON connected to it
            - Keeps track of files in those peers

    
### P2P network Case study 4: BitTorrent
![alt text](image-46.png)

- P2P Content Distribution
- BitTorrent builds a network (swarm) for every file that is being distributed
    - Initially, for each shared file, there is one server (seed) which hosts the original copy
        - File is broken into chunks
            - Can download from multiple peers (different chunk from different peer)
    - "torrent" file: metadata about the content
        - Hosted on a web server usually
    - Client downloads torrent file
        - Indicates sizes and checksums of chunks
        - Identifies a tracker


- **Big advantage over the previous 3: Can send "link" to a friend (.torrent file)**
    - "link" always refers to the same file
        - Acts as the unique identifier for a specific file
            - Other 3 P2P networks do not have this
            - Guarantee 1:1 correspondence (as opposed to filename, metadata matching)

#### Components of BitTorrent

1. Tracker
    - Server that keeps track of which seeds and peers are in the swarm
    - Does not participate in file distribution

2. Torrent
    - Group of peers exchanging chunks of a file
3. Swarm
    - Seeds + Peers

#### BitTorrent: Technical details

- File divided into 256KB chunks (Arbitrarily set, no particular reson)

- Peer joining torrent
    - Has no chunks initially
    - Will accumulate chunks over time
    - Registers with tracker to get a list of peers
        - Only connects to a subset of them ("neighbours")
    
- When downloading:
    - Peer uploads chunks to others

- Peers may come and go
    - Peer can leave (selfish) or remain (altruistic) after obtaining entire file

#### BitTorrent: Strategies
    - Pulling Chunks
        - At any given time, peers have different chunks
            - Periodically, peer asks neighbours for which chunks they have
                - Sends requests for missing chunks
                    - Rarest first
    - Pushing chunks: Tit-for-tat
        - Peer sends chunks to four neighbours currently sending peer chunk at highest rate
            - Periodically evaluate this top 4 every 10s
        - Every 30s randomly select another peer and start sending chunks
            - New peer may join top 4
            - "Optimistically un-choke"


### P2P: Key technologies for P2P lookup services


How do I find objects?
- Searching
    - Each object uniquely identifiable
        - Need unique identifier (like names)
    - Object locaiton can be made efficient
        - Need to maintain structure required for addressing
- Addressing
    - No need to know unique names
    - Hard to make efficient
    - Need to compare to actual objects to know if they are the same

Depends on:
- How network is formed
- Where objectives are placed
- How objects can be found efficiently


#### Two types of P2P

1. Unstructured Networks / Systems
    - Searching is required
    - Peers are free to:
        - Join anywhere
        - Choose neighbours freely
    - Objects are stored anywhere
2. Structured Networks / Systems
    - Allow for addressing / deterministic routing
    - Network structure determines where peers belong in the net and where objects are stored


#### Key-value Store

- Database contains entries in (key,value) pairs
    - Key: ID number, value: human name
    - Key: content name/type, value: IP addr

- Operations
    - Put(Key, value)
    - Get(key) -> value

- Looks like a table
    - Finding an object takes O(N)...
        - Use a Hash Table!
            - Insertion / Deletion / Lookup are all O(1)!

#### DHT (Distributed Hash Table)

![alt text](image-47.png)

Key idea: Distribute hash buckets to peers

Challenge: Design and implement efficient mechanism to:
- Find which peer is responsible for which hash bucket
- Route between peers

Principles
1. Each node is responsible for at least 1 bucket
    - Changes as nodes join and leave

2. Nodes communicate among themselves to find responsible node
    - DHT is efficient when communication is scalable

3. DHTs support all hash table operations

##### DHT Case Study: Chord

- Uses SHA-1 hash function
    - 160-bit identification for
        - Nodes
        - Objects
    - Same hash function for node and object
        - Node ID hash from IP address
        - Object ID hashed from object name

- Organized in a ring which wraps around
    - Nodes keep track of predecessor and successor
    - Think of hash ring in system design

- Assign identifier to each node / object in the range [0, $2^m - 1$] (This is the namespace)
    - Each identifier can be represented by m bits (160 in SHA-1)
    - Assign (key,value) pairs to nodes / peers
        - Assign to closest ID available
        - Convention is to use immediate successor
            - e.g Smallest integer larger than hash

**Simple example of 3 bits**

![alt text](image-48.png)

- How do I find a node? (Routing)
    - Generally takes O(N) steps
        - N = amount of nodes
        - Bad for large N.

- Solution: Add shortcut
    - Each node n maintains a finger table that
        - Includes at most m shortcuts
        - ith finger / shortcut is at least $2^{i-1}$ far apart

**Finger Table**: An example calculation

![alt text](image-49.png)

![alt text](image-50.png)

Node 3
| k | Calculation of start        | start | interval  | first node ≥ start |
|---|------------------------------|--------|-----------|---------------------|
| 1 | 3 + 2^0 = 4                  | 4      | [4, 5)    | 4                   |
| 2 | 3 + 2^1 = 5                  | 5      | [5, 7)    | 6                   |
| 3 | 3 + 2^2 = 7                  | 7      | [7, 3)    | 0                   |

Node 6
| k | Calculation of start        | start | interval  | first node ≥ start |
|---|------------------------------|--------|-----------|---------------------|
| 1 | 6 + 2^0 = 7                  | 7      | [7, 0)    | 0                   |
| 2 | 6 + 2^1 = 8 mod 8 = 0        | 0      | [0, 2)    | 0                   |
| 3 | 6 + 2^2 = 10 mod 8 = 2       | 2      | [2, 6)    | 2                   |



**Finger Table**: Example of Node Joining

![alt text](image-51.png)

**Consider this case, where only node 1 is here.**

Node 1:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 2      | [2, 3)    | 1                   |
| 3      | [3, 5)    | 1                   |
| 5      | [5, 1)    | 1                   |

**After Node 2 Joins: [1, 2]**

Node 1:
| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 2      | [2, 3)    | **2**                   |
| 3      | [3, 5)    | 1                   |
| 5      | [5, 1)    | 1                   |

Node 2:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 3      | [3, 4)    | 1                   |
| 4      | [4, 6)    | 1                   |
| 6      | [6, 2)    | 1                   |

**After Node 0, 6 Joins: [0,1,2,6]**

Node 0:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 1      | [1, 2)    | 1                   |
| 2      | [2, 4)    | 2                   |
| 4      | [4, 0)    | 6                   |

Node 1:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 2      | [2, 3)    | 2                   |
| 3      | [3, 5)    | 6                   |
| 5      | [5, 1)    | 6                   |

Node 2:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 3      | [3, 4)    | 6                   |
| 4      | [4, 6)    | 6                   |
| 6      | [6, 2)    | 6                   |

Node 6:

| start | interval  | first node ≥ start |
|--------|-----------|---------------------|
| 7      | [7, 0)    | 0                   |
| 0      | [0, 2)    | 0                   |
| 2      | [2, 6)    | 2                   |



**Routing**

Use same example: Nodes: [0,1,2,6]
Assume a node caches values that are < node.val (e.g 6 stores 3,4,5,6)

I Query node 1: hash(key) = 7

1. Since 7 > 1 and Since 5 <= 7 < 1 (+ 8): We query node 6
2. Since 7 > 6 and Since 7 <= 7 < 0 (+ 8): We query node 0
3. Since 0 (+ 8) > 7: We obtain our content from node 0's table.


**Node Leave**

To handle each node departure, each node must know the IP address of its two successors
- Each node periodically pings its 2 successors to see if they are still alive.

Example: [0,1,2,6]
- Peer 1 leaves.
- Peer 0 detects peer 1 leaving (ping no response)
    - Set immediate successor to 2
    - Set successor of successor to successor of 2 (6)