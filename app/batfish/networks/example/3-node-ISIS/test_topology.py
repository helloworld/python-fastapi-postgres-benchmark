from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.question import bfq
import pandas as pd

# Initialize the Batfish client
bf_session = Session(host='localhost')

# Initialize snapshot
NETWORK_NAME = "example"
SNAPSHOT_NAME = "3-node-isis"

# Load the snapshot
bf_session.set_network(NETWORK_NAME)
bf_session.init_snapshot(".", name=SNAPSHOT_NAME, overwrite=True)

def test_isis_adjacencies():
    """Test that ISIS adjacencies are established between neighbors"""
    isis_edges = bfq.layer3Edges().answer().frame()
    expected_edges = [
        ('r1', 'r2'),
        ('r2', 'r1'),
        ('r2', 'r3'),
        ('r3', 'r2')
    ]
    
    actual_edges = [(edge.node1, edge.node2) for edge in isis_edges['Edge']]
    for edge in expected_edges:
        assert edge in actual_edges, f"Missing ISIS adjacency between {edge[0]} and {edge[1]}"
    print("✓ ISIS adjacencies test passed")

def test_loopback_reachability():
    """Test that all routers can reach each other's loopbacks"""
    routers = ['r1', 'r2', 'r3']
    loopbacks = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
    
    for src_router in routers:
        for dst_ip in loopbacks:
            reachability = bf_session.q.reachability(
                pathConstraints=PathConstraints(
                    startLocation=src_router,
                    endLocation=".*",
                    transitLocations=".*",
                    finalNodesSpecifier=".*"
                ),
                headers=HeaderConstraints(dstIps=dst_ip)
            ).answer().frame()
            
            assert len(reachability) > 0, f"No reachability from {src_router} to {dst_ip}"
            flow_traces = reachability['Traces'][0]
            assert any(trace.disposition == 'ACCEPTED' for trace in flow_traces), \
                f"No successful path from {src_router} to {dst_ip}"
    
    print("✓ Loopback reachability test passed")

def test_interface_configuration():
    """Test that interfaces are properly configured with ISIS"""
    interfaces = bfq.interfaceProperties(nodes="/r./", properties=["Active", "Primary_Address", "ISIS_Enabled"]).answer().frame()
    
    # Check that all interfaces connecting routers have ISIS enabled
    connecting_interfaces = interfaces[interfaces['Interface'].str.contains('GigabitEthernet')]
    assert all(connecting_interfaces['ISIS_Enabled']), "Not all router interfaces have ISIS enabled"
    
    # Check that all interfaces are active
    assert all(interfaces['Active']), "Not all interfaces are active"
    print("✓ Interface configuration test passed")

if __name__ == "__main__":
    print("\nRunning tests for 3-node ISIS topology...")
    print("-" * 50)
    
    try:
        test_isis_adjacencies()
        test_loopback_reachability()
        test_interface_configuration()
        print("\nAll tests passed successfully! ✓")
    except AssertionError as e:
        print(f"\nTest failed: {str(e)}")
    except Exception as e:
        print(f"\nError running tests: {str(e)}")