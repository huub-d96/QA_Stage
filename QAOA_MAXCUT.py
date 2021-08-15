"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut
Description: Test script for enhanced rotation

"""

import xacc
import networkx as nx
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def genMaxcutCircuit(qpu, graph, params):
    
    compiler = xacc.getCompiler('xasm')
    circuit = '__qpu__ void qaoa_maxcut(qbit q){  \n'
    
    p = len(params)//2
    beta = params[:p]
    gamma = params[p:]
    
    #Set inital state to superposition
    for N in range(len(graph.nodes)):
        #H = provider.createInstruction('H', [N])
        #program.addInstructions([H])
        circuit += ('H(q[%i]); \n' % N)
    
    for P in range(p):  
            
        #For all edges, set cost Hamiltonian
        for E in graph.edges:
            #CNOT = provider.createInstruction('CX', [E[0], E[1]])
            #program.addInstructions([CNOT])
            
            #Rz = provider.createInstruction('Rz', [E[1]], [gamma[P]])               
            #program.addInstructions([Rz])
            
            #CNOT = provider.createInstruction('CX', [E[0], E[1]])
            #program.addInstructions([CNOT])
            
            circuit += ('CX(q[%i], q[%i]); \n' % (E[0], E[1]))
            circuit += ('Ry(q[%i], %f); \n' % (E[1], gamma[P]))
            circuit += ('CX(q[%i], q[%i]); \n' % (E[0], E[1]))
        
        #Apply mixer hamilonian to all qubits    
        for N in range(len(graph.nodes)):
            #Rx = provider.createInstruction('Rx', [N], [beta[P]])
            #program.addInstructions([Rx])
            circuit += ('Rx(q[%i], %f); \n' % (N, beta[P]))
            
    #Measure results
    for N in range(len(graph.nodes)):
        #M = provider.createInstruction('Measure', [N])
        #program.addInstructions([M])
        circuit += ('Measure(q[%i]); \n' % N)
        
    circuit += ('}')
        
    #print(circuit)     
        
    program = compiler.compile(circuit, qpu) 
        
    return program.getComposite('qaoa_maxcut')


def compute_expectation(counts, G):
    
    def maxcut_obj(x, G):

        obj = 0
        for i, j in G.edges():
            if x[i] != x[j]:
                obj -= 1
                
        return obj
    
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        
        obj = maxcut_obj(bitstring, G)
        avg += obj * count
        sum_count += count
        
    return avg/sum_count

def getOptFunction(qpu, graph):
        
    def execute_circ(params):
        
        program = genMaxcutCircuit(qpu, graph, params)
        qpu.execute(buffer, program)
        results = buffer.getMeasurementCounts()
        
        return compute_expectation(results, graph)
    
    return execute_circ

# Get access to the desired QPU and
# allocate some qubits to run on
#qpu = xacc.getAccelerator('aer', {'shots':1024})
qpu = xacc.getAccelerator('ibm:ibmq_qasm_simulator', {'shots': 1024})
#qpu = xacc.getAccelerator('ibm', {'backend':'ibmq_quito', 'shots': 1024})


# Construct graph
graph = nx.Graph()
graph.add_nodes_from([0, 1, 2, 3])
graph.add_edges_from([(0, 1), (1, 2), (2, 3), (0,3)])
nx.draw(graph, with_labels=True, alpha=0.8, node_size=500)

#print(graph)

#Setup QAOA variables
p = 1
buffer = xacc.qalloc(graph.size())

#Find optimal values
optFunc = getOptFunction(qpu, graph)
initParams = [1.0]*2*p
optResult = minimize(optFunc, initParams, method='COBYLA')
optParams = optResult.x
print(optResult)

#Show results
program = genMaxcutCircuit(qpu, graph, optParams)
qpu.execute(buffer, program)
results = buffer.getMeasurementCounts()

plt.figure()
plt.bar(results.keys(), results.values(), color='b')
plt.xticks(rotation=45, ha='right')
plt.show()




        
        
        