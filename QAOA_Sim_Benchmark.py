#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 14:18:34 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut
Description: Benchmark for simulators using QAOA

"""

import QAOA_MAXCUT as qaoa
import generate_graph as gg
import xacc
import networkx as nx

# Get access to the desired QPU and
# allocate some qubits to run on
qpu_id =  'ibm:ibmq_qasm_simulator' #'aer' #'ionq' #'qpp'  #'qsim'  
qpu = xacc.getAccelerator(qpu_id, {'shots':2048, 'name': 'QAOA'})

#Additional QuaC libraries
#backendJSON = open('backends.json', 'r').read()
#qpu.contributeInstructions(backendJSON)

# Construct and plot graph
size = 4
#g = gg.regular_graph(size)
g=[4, [[0,1],[1,2],[2,3],[3,0]]]
graph = nx.Graph()
graph.add_nodes_from(range(size))
graph.add_edges_from(g[1])
nx.draw_circular(graph, with_labels=True, alpha=0.8, node_size=500)


#Run QAOA
qaoa_result, ave_runtime = qaoa.runQAOA(qpu, qpu_id, graph) #List of 8 best solutions & average runtime

#Print results
print("QAOA: ", qaoa_result)
print("Average Runtime: ", ave_runtime)