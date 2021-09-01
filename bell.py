#Auhtor: Huub Donkers
#Date: 05-08-2021
#Project: Exploring XACC Framework
#Description: Test script to generate a bell pair

import xacc
import extra_gates as gates

#Setup qpu platform for two qubits
xacc.Initialize()
qpu = xacc.getAccelerator('rigetti-qvm')
n = 5
buffer = xacc.qalloc(n)

#Create quantum program
compiler = xacc.getCompiler('xasm')

circuit = "__qpu__ void bell(qbit q){ \n"
circuit += gates.dicke_init(n, 2, range(n))
circuit += '''
            Measure(q[0]);
            Measure(q[1]);
            Measure(q[2]);
            Measure(q[3]);
            Measure(q[4]);
            }
            '''

#circuit = '''__qpu__ void bell(qbit q){
#		H(q[0]);
#        Toffoli(q[0], q[1], q[2]);
#        
#        Measure(q[0]);
#        Measure(q[1]);
#		}'''

program = compiler.compile(circuit, qpu)

mapped_program = program.getComposite('bell')


#Execute and readout buffer
qpu.execute(buffer, mapped_program)

results = buffer.getMeasurementCounts()
#expZ = buffer.getExpectationValueZ()
print(results)
#print(expZ)\

# Finalize the framework
xacc.Finalize()

