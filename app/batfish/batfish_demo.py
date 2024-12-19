from pybatfish.client.commands import *
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
from pybatfish.question import *

# Initialize the Batfish service
NETWORK_NAME = "linear_3node_network"
SNAPSHOT_NAME = "snapshot_1"
SNAPSHOT_DIR = "networks/example/linear-3node-isis-ibgp"

# Initialize Batfish and load the snapshot
bf_session.host = "localhost"
bf_init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)
bf_set_network(NETWORK_NAME)

# Get a list of all nodes in the network
node_properties = bfq.nodeProperties().answer().frame()
print("\nNodes in network:")
print(node_properties[["Node", "Configuration_Format"]])

# Initialize a reachability question from r1 to r3
reachability = bfq.reachability(
    pathConstraints=PathConstraints(
        startLocation="r1",
        endLocation="r3"
    )
)

# Get the answer
answer = reachability.answer()
print("\nReachability results:")
print(answer.frame())

# Let's also check the status of all interfaces
interfaces = bfq.interfaceProperties().answer().frame()
print("\nInterface status:")
print(interfaces[["Interface", "Active", "Primary_Address"]])