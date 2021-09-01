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
import runtime_plots as plot

# Get access to the desired QPU and
# allocate some qubits to run on
#qpu = xacc.getAccelerator('ibm:ibmq_manila', {'shots': 4096})
#qpu = xacc.getAccelerator('ibm', {'backend':'ibmq_manila', 'shots': 4096})
#qpu = xacc.getAccelerator('ionq', {'shots':5000})
qpu_id = 'aer'
qpu = xacc.getAccelerator(qpu_id, {'shots': 2048})
problem = 'maxcut'
p = 2
size = 4

# Construct and plot graph
if(problem !='TSP'):
    #graph = gg.regular_graph(size)
    graph = [4, [[0,1],[1,2], [2,3], [3,0]]]
    plot.draw_graph(graph)
else:
    graph = gg.tsp_problem_set(size, gg.regular_graph)    
    #TODO: DRAW network


#Run QAOA
qaoa_result, runtimes = qaoa.runQAOA(qpu, qpu_id, graph, problem, p) #List of 8 best solutions

#Run exact solver
if(problem == 'maxcut'):
    exact_result = exact.mcp_solver(graph)
elif(problem == 'TSP'):
    max_score, exact_result = exact.tsp_score(graph)


#Print results
print("QAOA: ", qaoa_result)
print("Exact: ", exact_result)

print("Match: ", len(list(set(qaoa_result) & set(exact_result))))