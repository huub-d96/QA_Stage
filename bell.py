#Auhtor: Huub Donkers
#Date: 05-08-2021
#Project: Exploring XACC Framework
#Description: Test script to generate a bell pair

import xacc

#Setup qpu platform for two qubits
ibm_backend = 'ionq'
qpu = xacc.getAccelerator(ibm_backend)
buffer = xacc.qalloc(2)

#Create quantum program
compiler = xacc.getCompiler('xasm')
circuit = '''__qpu__ void bell(qbit q){
		H(q[0]);
        CX(q[0], q[1]);
        
        Measure(q[0]);
        Measure(q[1]);
		}'''

program = compiler.compile(circuit, qpu)

mapped_program = program.getComposite('bell')


#Execute and readout buffer
qpu.execute(buffer, mapped_program)

results = buffer.getMeasurementCounts()
#expZ = buffer.getExpectationValueZ()
print(results)
#print(expZ)\

# from qiskit import IBMQ    

# #Receive IBM job results via qiskit
# provider = IBMQ.load_account()
# backend = provider.get_backend(ibm_backend)
# ID = buffer.getInformation().get('ibm-job-id')
# job = backend.retrieve_job(ID)

# #Compute runtime
# times = job.time_per_step()
# runtime = times.get('COMPLETED') - times.get('RUNNING')

# print(runtime.total_seconds())

