to run:
    python OSPF.py -f inpfile -o outfile -h HELLO_INTERVAL -a LSA_INTERVAL -s SPF_INTERVAL

where 
    inpfile : name of input file
    outfile : name of outfile . Ex: if outfile = "Node" then each routers output file is name as "Node _1.txt", "Node_2.txt" and so on
    HELLO_INTERVAL : time between sending of hello packets by a router (in seconds)
    LSA_INTERVAL : time between sending of LSA packets by a router (in seconds)
    SPF_INTERVAL : time between each dijkstras implementation by a router (in seconds)

Here instead of opening N terminals for each router, I have used multiprocessing so runnins OSPF.py will create N routers as N processes on its own.

Input file Format:

No_of_Vertices  No_of_edges
Edge_1_from Edge_1_to min_cost max_cost
Edge_2_from Edge_2_to min_cost max_cost
Edge_3_from Edge_3_to min_cost max_cost
Edge_4_from Edge_4_to min_cost max_cost
.
.
.
.