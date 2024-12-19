from pybatfish.client.session import Session
from pybatfish.datamodel import *

# Initialize the Batfish client
bf_session = Session(host='localhost')

# Initialize snapshot
NETWORK_NAME = "example"
SNAPSHOT_NAME = "isis-4-node"  # Changed this to match our directory name

# Load the example snapshot
bf_session.set_network(NETWORK_NAME)
bf_session.init_snapshot("../networks/example/isis-4-node", name=SNAPSHOT_NAME, overwrite=True)

# First, let's check the routes on r1
routes = bf_session.q.routes(nodes="r1").answer().frame()
print("\nRoutes on r1:")
print("-" * 50)
print(routes)

# Run reachability question
print("\nRunning reachability from r1 to r4...")
reachability = bf_session.q.reachability(
    pathConstraints=PathConstraints(
        startLocation="host1",
        endLocation="host2"
    )
).answer()

# Get the reachability result frame
reach_frame = reachability.frame()
print(reach_frame)

# Print detailed information about each reachability flow
print("\nReachability Results:")
print("-" * 50)
for index, row in reach_frame.iterrows():
    print("\nFlow Details:")
    print("-" * 50)
    for column in reach_frame.columns:
        print(f"{column}:")
        print(row[column])
        print("-" * 50)

# Now run traceroute from r1 to r4's loopback
#print("\nRunning traceroute from r1 to 4.4.4.4...")
#traceroute = bf_session.q.traceroute(
#    startLocation="r1",
#    headers=HeaderConstraints(
#        dstIps="4.4.4.4"
#    )
#).answer()
#
## Get the traceroute result frame
#trace_frame = traceroute.frame()
#
## Print all traces
#print("\nAll Traces from r1 to r4:")
#print("-" * 50)
#for trace in trace_frame['Traces'][0]:
#    print()
#    print(trace)
#    print()
