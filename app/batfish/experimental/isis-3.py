from pybatfish.client.session import Session
from pybatfish.datamodel import *

# Initialize the Batfish client
bf_session = Session(host='localhost')

# Initialize snapshot
NETWORK_NAME = "example"
SNAPSHOT_NAME = "live"

# Load the example snapshot
bf_session.set_network(NETWORK_NAME)
bf_session.init_snapshot("../networks/example/3-node-isis", name=SNAPSHOT_NAME, overwrite=True)

# Run a simple reachability question using bf_session.q instead of bfq
reachability = bf_session.q.reachability(
    pathConstraints=PathConstraints(
        startLocation="r1",
        endLocation="r3"
    )
).answer()

# Get the result frame
result_frame = reachability.frame()

# Print detailed information about each flow
for index, row in result_frame.iterrows():
    print("\nFlow Details:")
    print("-" * 50)
    for column in result_frame.columns:
        print(f"{column}:")
        print(row[column])
        print("-" * 50)

for t in result_frame['Traces'][0]:
    print()
    print(t)
    print()
