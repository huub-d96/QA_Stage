#Auhtor: Huub Donkers
#Date: 05-08-2021
#Project: Exploring XACC Framework
#Description: Test script to generate a bell pair

import xacc

#Setup qpu platform for two qubits
qpu = xacc.getAccelerator('aer')
buffer = xacc.qalloc(2)

#Create quantum program
compiler = xacc.getCompiler('xasm')
circuit = '''__qpu__ void bell(qbit q){
		H(q[0]);
		CX(q[0],q[1]);
		Measure(q[0]);
		Measure(q[1]);
		}'''

program = compiler.compile(circuit, qpu)

#Execute and readout buffer
qpu.execute(buffer, program.getComposites()[0])
results = buffer.getMeasurementCounts()
expZ = buffer.getExpectationValueZ()
print(results)
print(expZ)
