from pybatfish.client.session import Session
from pybatfish.datamodel import *

# Initialize the Batfish client
bf_session = Session(host='localhost')

# Initialize snapshot
NETWORK_NAME = "example"
SNAPSHOT_NAME = "3-node-bgp"

# Load the snapshot
bf_session.set_network(NETWORK_NAME)
bf_session.init_snapshot("networks/example/3-node-bgp", name=SNAPSHOT_NAME, overwrite=True)

def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

# Test 1: BGP Session Status
print_section("BGP Session Status")
bgp_sessions = bf_session.q.bgpSessionStatus().answer().frame()
print(bgp_sessions)

# Test 2: BGP Peer Configuration
print_section("BGP Peer Configuration")
bgp_peers = bf_session.q.bgpPeerConfiguration().answer().frame()
print(bgp_peers)

# Test 3: Node-to-Node Reachability Tests
def test_reachability(start, end, expected_established=True):
    print_section(f"Reachability Test: {start} -> {end}")
    reachability = bf_session.q.reachability(
        pathConstraints=PathConstraints(
            startLocation=start,
            endLocation=end
        )
    ).answer().frame()
    
    print(f"Flows from {start} to {end}:")
    if len(reachability['Traces']) > 0 and len(reachability['Traces'][0]) > 0:
        for t in reachability['Traces'][0]:
            print(t)
            print()
    else:
        print("No traces found - connectivity failed")

# Test all node pairs
node_pairs = [
    ("r1", "r2"),  # Should work via ISIS/iBGP
    ("r2", "r1"),  # Should work via ISIS/iBGP
    ("r2", "r3"),  # Should work via eBGP
    ("r3", "r2"),  # Should work via eBGP
    ("r1", "r3")  # Should work via r2
    #("r3", "r1")   # Should work via r2
]

for start, end in node_pairs:
    test_reachability(start, end)

# Comment out the problematic BGP routes section
# print_section("BGP Routes")
# routes = bf_session.q.routes(nodes=".*", protocols=["BGP"]).answer().frame()
# print(routes)

# Test 5: IP Owners (to verify interface configuration)
print_section("IP Owners")
ip_owners = bf_session.q.ipOwners().answer().frame()
print(ip_owners)

# Add a specific function to check r2's routes
def check_r2_routes():
    print_section("R2's Routes")
    routes = bf_session.q.routes(nodes="r2").answer().frame()
    
    print("\nRoutes on r2:")
    print("-" * 40)
    for index, route in routes.iterrows():
        print(f"Network: {route['Network']}")
        print(f"Protocol: {route['Protocol']}")
        print(f"Next Hop: {route['Next_Hop']}")
        print("-" * 40)

def check_r3_routes():
    print_section("R3's Routes")
    routes = bf_session.q.routes(nodes="r3").answer().frame()
    
    print("\nRoutes on r3:")
    print("-" * 40)
    for index, route in routes.iterrows():
        print(f"Network: {route['Network']}")
        print(f"Protocol: {route['Protocol']}")
        print(f"Next Hop: {route['Next_Hop']}")
        print("-" * 40)

def check_bgp_routes():
    print_section("BGP Routes on all routers")
    routes = bf_session.q.routes(protocols="bgp").answer().frame()
    
    print("\nBGP Routes:")
    print("-" * 40)
    for index, route in routes.iterrows():
        print(f"Node: {route['Node']}")
        print(f"Network: {route['Network']}")
        print(f"Protocol: {route['Protocol']}")
        print(f"Next Hop: {route['Next_Hop']}")
        if 'AS_Path' in route:
            print(f"AS Path: {route['AS_Path']}")
        print("-" * 40)

# Add r2 and r3 route checks at the end
check_r2_routes()
check_r3_routes()
check_bgp_routes()
