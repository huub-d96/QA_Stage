#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 20:29:26 2021

@author: huub
"""

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.ticker import MaxNLocator

def plot_iterations(backend_runtimes):
    return

def draw_graph(g):
    
    graph = nx.Graph()
    graph.add_nodes_from(range(g[0]))
    graph.add_edges_from(g[1])
    nx.draw_circular(graph, with_labels=True, alpha=0.8, node_size=500)
    
    return

def lineplot_results(backend_runtimes, graph_sizes, title, legend = []):
    fig = plt.figure(num =1, figsize=(7,5))
    ax = fig.gca()
    
    backend_means = []
    for runtimes_list in backend_runtimes:
        means = []
        for runtimes in runtimes_list:
            means.append(sum(runtimes)/len(runtimes))
        ax.plot(graph_sizes, means, marker = 'o')   
      
    
    # Force x-axis integers
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    #y-axis scale
    plt.yscale("log")
    #ax.set_ylim([10**(-1), 10**6])
     
    # Adding title
    plt.title(title)
    plt.xlabel("Nodes")
    plt.ylabel("Runtime [ms]")
    
    #Add legend
    for qpu in legend:
        if qpu in ['aer', 'qsim']:
            qpu = qpu+' (local)'
    plt.legend(legend, bbox_to_anchor=(1, 0.9), loc = 'upper right')
     
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    


def boxplot_results(runtimes_list, graph_sizes, title):
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
    plt.title(title)
    plt.xlabel("Nodes")
    plt.ylabel("Runtime [ms]")
     
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
         
    # show plot
    plt.show(bp)
    
    return 