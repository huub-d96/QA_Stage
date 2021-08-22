def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def mcp_solver(g):
    result = 0
    array = []
    size, edges = g
    for n in range(2**size):
        node_array = bitfield(n)         
        node_array = [0]*(size-len(node_array)) + node_array    
        #node_array.extend([0]*(size-len(node_array)))
        node_array = [-1 if x == 0 else 1 for x in node_array]
        
        
        c = 0
        for e in edges:
            c += 0.5 * (1 - int(node_array[e[0]]) * int(node_array[e[1]]))
           
        if c >= result:
            if c > result:
                array.clear()   
            array.append(''.join(map(str, [0 if x == -1 else 1 for x in node_array])))    
            result = c  
        #print(array)             
        
    return array
