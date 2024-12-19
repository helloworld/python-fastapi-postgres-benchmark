# Context:
Batfish's architecture has two main phases:
1. Modeling Phase (Top Half): Ingests router configs and simulates router behavior
2. Verification Phase (Bottom Half): Takes modeled inputs and performs formal verification
3. The code that you are tasked to explore and is relevant to answer the task is located at app/batfish

# Objective:
A user would like to remove batfish's top half and directly provide inputs to its verification engine. The user is interested in focusing on the reachability query as a starting point to understand the interface between these phases. Your job as an agent is to help the user make a list of files which contain relevant code to accomplish the specified task so that they can explore the relevant code quickly.

Specific Questions:
1. What are the essential data structures and fields needed to interface directly with the verification engine?
2. Which source files should I examine to understand and modify this interface?

# Instructions: 
1. carefully consider the objective you have been given and read through relevant files in app/batfish.
2. identify files and functions in the code which are relevant/important to bypassing the modeling phase entirely by directly providing the necessary data structures (like FIB/AFT entries) to the verification engine. you can assume we have access to AFT forwarding entries and also openconfig formatted config files.
3. think about how the files and functions relate to each other. 
4. once you have a complete list of files and functions, identify the files they are located in and write the files a user should look at to quickly get up to speed in app/files_to_explore.txt.
5. ONLY include filepaths in the .txt output file you make. reason extensively about what functions are relevant and how they play with other classes, but do NOT include this analysis in the output .txt results file you write to.

# Required Output:
Create a file at app/files_to_explore.txt containing one absolute file path per line for files relevant to this exploration. Example format:
./app/batfish/projects/batfish/src/test/java/org/batfish/grammar/cisco_asa/CiscoAsaGrammarTest.java

Note: Include ALL paths to files that are directly relevant to understanding or modifying the interface between Batfish's modeling and verification phases. Let's focus on the reachability query as a starting point to understand the interface between these phases.

# Evaluation:
Correctness of your exploration will be evaluated by running pytest app/tests/test.py. do NOT look at this test file, since it contains the answers.
