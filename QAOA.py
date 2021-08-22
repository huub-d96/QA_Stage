"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut, travellings salesman and dominating set problem
Description: QAOA functions

"""

import xacc
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import time

def genTSPCircuit(qpu, qpu_id, graph, params):
    
    return 0

def getTSPExpectation(counts, graph):
    
    return 0

def genDSPCircuit(qpu, qpu_id, graph, params):
    
    return 0

def getDSPExpectation(counts, graph):
    
    return 0

def genMaxcutCircuit(qpu, qpu_id, graph, params):
    
    compiler = xacc.getCompiler('xasm')
    circuit = '__qpu__ void qaoa_maxcut(qbit q){  \n'
    
    p = len(params)//2
    beta = params[:p]
    gamma = params[p:]
    
    #Set inital state to superposition
    for N in range(len(graph.nodes)):
        circuit += ('H(q[%i]); \n' % N)
    
    for P in range(p):  
            
        #For all edges, set cost Hamiltonian
        for E in graph.edges:            
            circuit += ('CX(q[%i], q[%i]); \n' % (E[0], E[1]))
            circuit += ('Ry(q[%i], %f); \n' % (E[1], gamma[P]))
            circuit += ('CX(q[%i], q[%i]); \n' % (E[0], E[1]))
        
        #Apply mixer hamilonian to all qubits    
        for N in range(len(graph.nodes)):
            circuit += ('Rx(q[%i], %f); \n' % (N, beta[P]))
            
    #Measure results
    for N in range(len(graph.nodes)):
        circuit += ('Measure(q[%i]); \n' % N)
        
    circuit += ('}')
        
    #print(circuit)     
        
    program = compiler.compile(circuit, qpu)
    
    mapped_program = program.getComposite('qaoa_maxcut')
    if(qpu_id[0:3] == 'ibm'):
        mapped_program.defaultPlacement(qpu)
        
    return mapped_program


def getMaxcutExpectation(counts, graph):
    
    def maxcut_obj(x, graph):

        obj = 0
        for i, j in graph.edges():
            if x[i] != x[j]:
                obj -= 1
                
        return obj
    
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        
        obj = maxcut_obj(bitstring, graph)
        avg += obj * count
        sum_count += count
        
    return avg/sum_count

def getOptFunction(qpu, graph, buffer, qpu_id, problem, runtimes):
        
    def execute_circ(params):
        
        if(problem == 'maxcut'):
            program = genMaxcutCircuit(qpu, qpu_id, graph, params)
        elif(problem == 'TSP'):
            program = genTSPCircuit(qpu, qpu_id, graph, params)
        elif(problem == 'DSP'):
            program = genDSPCircuit(qpu, qpu_id, graph, params)
        else:
            print('Unknown problem set: Exit...')
            quit()
        
        start = time.time()
        qpu.execute(buffer, program)        
        runtimes.append(getRuntime(qpu_id, buffer, start))
        results = buffer.getMeasurementCounts()
        
        if(problem == 'maxcut'):
            expectation = getMaxcutExpectation(results, graph)
        elif(problem == 'TSP'):
            expectation = getTSPExpectation(results, graph)    
        elif(problem == 'DSP'):
            expectation = getDSPExpectation(results, graph)        
        else:
            print('Unknown problem set: Exit...')
            quit()    
        
        return expectation
    
    return execute_circ

def getRuntime(qpu_id, buffer, start):
    
    '''
    Returns runtime of a backend in ms
    '''
    
    runtime = 0
    end = time.time()
    
    #IBM runtimes:  
    if(qpu_id[0:3] == 'ibm'): #Remote runtime
        
        from qiskit import IBMQ 
        #Receive IBM job results via qiskit
        ibm_backend = qpu_id[4:]
        provider = IBMQ.load_account()
        backend = provider.get_backend(ibm_backend)
        ID = buffer.getInformation().get('ibm-job-id')
        job = backend.retrieve_job(ID)
        
        #Compute runtime
        times = job.time_per_step()
        timeDelta = times.get('COMPLETED') - times.get('RUNNING')
        runtime = timeDelta.total_seconds()*1000 #s to ms
    
    elif(qpu_id == 'ionq'):
        import requests
        key = open('/home/huub/.ionq_config').readline().split(':')[1].strip()
        headers = {'Authorization': 'apiKey '+str(key)}
        params = {'limit': 1} #Only retrieve most recent execution
        response = requests.get('https://api.ionq.co/v0.1/jobs/', headers=headers, params=params)
        runtime = response.json().get('jobs')[0].get('execution_time')
    
    elif(qpu_id in ['aer', 'qsim', 'qpp']): #Local runtime
        runtime = (end - start)*1000 #s to ms
        
    else:
        print("Unkown QPU ID!")
        quit()
    
    return runtime

def runQAOA(qpu, qpu_id, graph, problem, p):
    
    #Setup QAOA variables
    buffer = xacc.qalloc(graph.number_of_nodes())
    
    #Find optimal values
    runtimes = []
    optFunc = getOptFunction(qpu, graph, buffer, qpu_id, problem, runtimes)
    initParams = [1.0]*2*p
    optResult = minimize(optFunc, initParams, method='COBYLA')
    optParams = optResult.x
    
    #Show results
    program = genMaxcutCircuit(qpu, qpu_id, graph, optParams)
    qpu.execute(buffer, program)
    results = buffer.getMeasurementCounts()
    
    #Plot results
    plt.figure()
    plt.bar(results.keys(), results.values(), color='b')
    plt.xticks(rotation=45, ha='right')
    plt.show()
    
    #Sort results
    results = dict(sorted(results.items(), key = lambda item: item[1], reverse=True)) #Return sorted list
    result_list = [k for k in results.keys()]
    
    return result_list[:8], runtimes




        
        
        