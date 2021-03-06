#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 21:22:07 2021

@author: huub
"""
from math import pi, acos, sqrt

def rxx(theta, q0, q1):
    
    circuit = "//RXX: \n"
    
    circuit += ('H(q[%i]); \n' % q0)
    circuit += ('H(q[%i]); \n' % q1)
    
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    circuit += ('Rz(q[%i], %f); \n' % (q1, theta))
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    
    circuit += ('H(q[%i]); \n' % q0)
    circuit += ('H(q[%i]); \n' % q1)    
    
    return circuit

def ryy(theta, q0, q1):
    
    circuit = "//RYY: \n"
    
    circuit += ('Rx(q[%i], %f); \n' % (q0, pi/2))
    circuit += ('Rx(q[%i], %f); \n' % (q1, pi/2))
    
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    circuit += ('Rz(q[%i], %f); \n' % (q1, theta))
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    
    circuit += ('Rx(q[%i], %f); \n' % (q0, -pi/2))
    circuit += ('Rx(q[%i], %f); \n' % (q1, -pi/2))
    
    return circuit

def rzz(theta, q0, q1):
    
    circuit = "//RZZ: \n"
    
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    circuit += ('Rz(q[%i], %f); \n' % (q1, theta))
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    
    return circuit

def toffoli(q0, q1, q2):
    
    circuit = "//toffoli: \n"
    
    circuit += ('H(q[%i]); \n' % q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q1, q2))
    circuit += ('Tdg(q[%i]); \n' % q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q2))
    circuit += ('T(q[%i]); \n' % q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q1, q2))
    circuit += ('Tdg(q[%i]); \n' % q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q2))
    circuit += ('T(q[%i]); \n' % q1)
    circuit += ('T(q[%i]); \n' % q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    circuit += ('H(q[%i]); \n' % q2)
    circuit += ('T(q[%i]); \n' % q0)
    circuit += ('Tdg(q[%i]); \n' % q1)
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    
    return circuit

def cry(theta, q0, q1):
    
    circuit = "//cry: \n"
    
    circuit += ('Ry(q[%i], %f); \n' % (q0, (pi/2)-theta/2))
    circuit += ('CX(q[%i], q[%i]); \n' % (q1, q0))
    circuit += ('Ry(q[%i], %f); \n' % (q0, -((pi/2)-theta/2)))

    return circuit


def ccry(theta, q0, q1, q2):
    
    circuit = "//ccry: \n"
    
    circuit += toffoli(q0, q1, q2)
    circuit += ('Ry(q[%i], %f); \n' % (q2, -theta/2))
    circuit += toffoli(q0, q1, q2)
    circuit += ('Ry(q[%i], %f); \n' % (q2, theta/2))
        
    return circuit


def scs(n, k, qbits):
    
    circuit = "//scs: \n"
    
    circuit += ('CX(q[%i], q[%i]); \n' % (qbits[n-2], qbits[n-1]))
    theta = 2 * (acos(sqrt(1 / n)))
    circuit += cry(theta, qbits[n-2], qbits[n-1])
    circuit += ('CX(q[%i], q[%i]); \n' % (qbits[n-2], qbits[n-1]))
    
    for m in range(k-1):
        l = 2+m
        control = n-2-m
        circuit += ('CX(q[%i], q[%i]); \n' % (qbits[control-1], qbits[n-1]))
        theta = 2 * (acos(sqrt((n-control) / n)))
        circuit += ccry(theta, qbits[n-1], qbits[control], qbits[control-1])
        
        circuit += ('CX(q[%i], q[%i]); \n' % (qbits[control-1], qbits[n-1]))        
    
    return circuit


def dicke_init(n, k, qbits):
    #deterministic  Dicke state preparation (B??rtschi & Eidenbenz, 2019)
    #unoptimized version
    
    circuit = "//Dicke: \n"
    
    for x in range(n-k, n):
        circuit += ('X(q[%i]); \n' % qbits[x])
    
    for i in range(n, k, -1):
        circuit += scs(i, k, qbits[0:i])
    
    for i in range(k, 1, -1):
        circuit += scs(i, i-1, qbits[0:i])
        
    return circuit  

def OR_2q(q0, q1, q2):
    
    circuit = "//OR_2q: \n"
    
    circuit += toffoli(q0, q1, q2)
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q1))
    circuit += ('CX(q[%i], q[%i]); \n' % (q0, q2))
    
    return circuit

def OR_nrz(n, gamma, qbits):
    
    circuit = "//OR_nrz: \n"
    
    circuit += OR_2q(qbits[0], qbits[1], qbits[n])
    
    for i in range(2, n):
        circuit += OR_2q(qbits[i], qbits[n+i-2], qbits[n+i-1])
    
    circuit += ('CRZ(q[%i], q[%i], %f); \n' % (2*n-2, 2*n-1, gamma))
    
    for i in range(n, 2, -1):
        circuit += OR_2q(qbits[n-i-1], qbits[2*n-2-i], qbits[2*n-1-i])
    
    circuit += OR_2q(qbits[0], qbits[1], qbits[n])
    
    return circuit