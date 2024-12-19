Task: Help identify the key files needed to bypass Batfish's modeling phase and directly provide inputs to its verification engine.
Let's focus on the reachability query as a starting point to understand the interface between these phases.

Context:
Batfish's architecture has two main phases:
1. Modeling Phase (Top Half): Ingests router configs and simulates router behavior
2. Verification Phase (Bottom Half): Takes modeled inputs and performs formal verification
3. The code that you are tasked to explore and is relevant to answer the task is located at app/batfish

Goal:
I want to bypass the modeling phase entirely by directly providing the necessary data structures (like FIB/AFT entries) to the verification engine.

Specific Questions:
1. What are the essential data structures and fields needed to interface directly with the verification engine?
2. Which source files should I examine to understand and modify this interface?

Required Output:
Create a file at app/files_to_explore.txt containing one absolute file path per line for files relevant to this exploration. Example format:
./app/batfish/projects/batfish/src/test/java/org/batfish/grammar/cisco_asa/CiscoAsaGrammarTest.java

Note: Include ALL paths to files that are directly relevant to understanding or modifying the interface between Batfish's modeling and verification phases. Let's focus on the reachability query as a starting point to understand the interface between these phases.

Evaluation: Correctness of your exploration will be evaluated by running pytest app/tests/test.py. do NOT look at this test file, since it contains the answers.
