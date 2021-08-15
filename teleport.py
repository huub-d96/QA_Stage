"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: Exploring XACC Framework
Description: Test script for quantum teleportation 

"""


import xacc

#Setup qpu platform for two qubits
qpu = xacc.getAccelerator('ibm:ibmq_quito', {'shots':2048})
buffer = xacc.qalloc(3)

#Create quantum program
compiler = xacc.getCompiler('xasm')
circuit = '''
        __qpu__ void teleport(qbit q){
        
            //Initialize teleported qubit to 1
            X(q[0]);
            
            //Create entangled pair between Alice and Bob
    		H(q[1]);
    		CX(q[1],q[2]);
            
            //Perform measurements (Alice)
            CX(q[0],q[1]);
            H(q[0]);
    		Measure(q[0]);
    		Measure(q[1]);
            
            //Corrections (Bob)
            if (q[0]){ Z(q[2]);}
            if (q[1]){ X(q[2]);}
            
            // Measure teleported qubit
            Measure(q[2]);
		}
        '''

program = compiler.compile(circuit, qpu)

#Execute and readout buffer
qpu.execute(buffer, program.getComposite('teleport'))
results = buffer.getMeasurementCounts()
print(results)
