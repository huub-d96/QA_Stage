"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut
Description: Benchmark for QAOA vs classical solver

"""

import QAOA as qaoa
import exact_solver as exact
import generate_graph as gg
import xacc
import networkx as nx

# Get access to the desired QPU and
# allocate some qubits to run on
#qpu = xacc.getAccelerator('ibm:ibmq_manila', {'shots': 4096})
#qpu = xacc.getAccelerator('ibm', {'backend':'ibmq_manila', 'shots': 4096})
#qpu = xacc.getAccelerator('ionq', {'shots':5000})
qpu_id = 'aer'
qpu = xacc.getAccelerator(qpu_id)
problem = 'TSP'
p = 2
size = 3

# Construct and plot graph
if(problem !='TSP'):
    g = gg.regular_graph(size)
    graph = nx.Graph()
    graph.add_nodes_from(range(size))
    graph.add_edges_from(g[1])
    nx.draw_circular(graph, with_labels=True, alpha=0.8, node_size=500)
else:
    graph = gg.tsp_problem_set(size, gg.regular_graph)    
    #TODO: DRAW network


#Run QAOA
qaoa_result, runtimes = qaoa.runQAOA(qpu, qpu_id, graph, problem, p) #List of 8 best solutions

#Run exact solver
if(problem == 'maxcut'):
    exact_result = exact.mcp_solver(g)
elif(problem == 'TSP'):
    max_score, exact_result = exact.tsp_score(graph)


#Print results
print("QAOA: ", qaoa_result)
print("Exact: ", exact_result)

print("Match: ", len(list(set(qaoa_result) & set(exact_result))))