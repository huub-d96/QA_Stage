#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 12:31:58 2021

Auhtor: Huub Donkers
Project: QAOA for maxcut
Description: Benchmark for IonQ simulator

"""

import QAOA as qaoa
import generate_graph as gg
import xacc
import networkx as nx
import matplotlib.pyplot as plt

# Get access to the desired QPU and
# allocate some qubits to run on
qpu_id = 'aer' #'ionq' 
qpu = xacc.getAccelerator(qpu_id, {'shots':2048})

graph_sizes = [3] #[4, 5, 6 , 7, 8]
runtimes_list = []

#Run QAOA
problem = 'TSP' #maxcut TODO: TSP, DSP
p = 3

for size in graph_sizes:    
       
    if(problem =='maxcut'):
        g = gg.regular_graph(size)
        graph = nx.Graph()
        graph.add_nodes_from(range(size))
        graph.add_edges_from(g[1])
        nx.draw_circular(graph, with_labels=True, alpha=0.8, node_size=500)
    else:
        graph = gg.tsp_problem_set(size, gg.regular_graph)    
        #TODO: DRAW network
        
    
    qaoa_result, runtimes = qaoa.runQAOA(qpu, qpu_id, graph, problem, p) #List of 8 best solutions & average runtime
    
    #Print results
    print("QAOA: ", qaoa_result)
    runtimes_list.append(runtimes)
    #print("Average Runtime: ", ave_runtime)

#Plot data

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)
 
# Creating axes instance
bp = ax.boxplot(runtimes_list, patch_artist = True)
 
colors = ['#0000FF', '#00FF00',
          '#FFFF00', '#FF00FF']
 
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
 
# changing color and linewidth of
# whiskers
for whisker in bp['whiskers']:
    whisker.set(color ='#8B008B',
                linewidth = 1.5,
                linestyle =":")
 
# changing color and linewidth of
# caps
for cap in bp['caps']:
    cap.set(color ='#8B008B',
            linewidth = 2)
 
# changing color and linewidth of
# medians
for median in bp['medians']:
    median.set(color ='red',
               linewidth = 3)
 
# changing style of fliers
for flier in bp['fliers']:
    flier.set(marker ='D',
              color ='#e7298a',
              alpha = 0.5)
     
# x-axis labels
ax.set_xticklabels(graph_sizes)

#y-axis scale
plt.yscale("linear")
 
# Adding title
plt.title("Problem: "+str(problem)+", Backend: "+str(qpu_id) + " simulator, Runtime for different N, p = " + str(p))
plt.xlabel("Nodes")
plt.ylabel("Runtime [ms]")
 
# Removing top axes and right axes
# ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
     
# show plot
plt.show(bp)