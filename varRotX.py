"""
Created on Thu Aug  5 12:05:10 2021

Auhtor: Huub Donkers
Project: Exploring XACC Framework
Description: Test script for enhanced rotation

"""


import xacc

#Setup qpu platform for two qubits
#qpu = xacc.getAccelerator('aer')
qpu = xacc.getAccelerator('ibm', {'backend':'ibmq_qasm_simulator'})
buffer = xacc.qalloc(1)

theta = 1.57

#Create quantum program
xacc.qasm('''
.compiler xasm
.circuit var_rotX
.parameters theta
.qbit q

Rx(q[0], '''+ str(theta) +''');
Measure(q[0]);
        ''')

print(qpu)
print(buffer)
program  = xacc.getCompiled('var_rotX')
print(program)

qpu.execute(buffer, program)
print(buffer)