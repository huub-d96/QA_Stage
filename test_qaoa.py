"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut
Description: Benchmark for QAOA vs classical solver

"""

import QAOA_MAXCUT as qaoa
import exact_solver as exact
import generate_graph as gg
import xacc
import networkx as nx

# Get access to the desired QPU and
# allocate some qubits to run on
#qpu = xacc.getAccelerator('aer', {'shots':5000})
qpu = xacc.getAccelerator('ibm:ibmq_manila', {'shots': 4096})
#qpu = xacc.getAccelerator('ibm', {'backend':'ibmq_manila', 'shots': 4096})
#qpu = xacc.getAccelerator('ionq', {'shots':5000})

# Construct and plot graph
size = 4
#g = gg.regular_graph(size)
g=[4, [[0,1],[1,2],[2,3],[3,0]]]
graph = nx.Graph()
graph.add_nodes_from(range(size))
graph.add_edges_from(g[1])
nx.draw_circular(graph, with_labels=True, alpha=0.8, node_size=500)


#Run QAOA
qaoa_result = qaoa.runQAOA(qpu, graph) #List of 8 best solutions

#Run exact solver
exact_result = exact.mcp_solver(g)


#Print results
print("QAOA: ", qaoa_result)
print("Exact: ", exact_result)

print("Match: ", len(list(set(qaoa_result) & set(exact_result))))