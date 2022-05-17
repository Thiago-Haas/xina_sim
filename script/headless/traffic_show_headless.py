import networkx as nx
import matplotlib.pyplot as plt

network_size=4

def generate_binary_network(binary_array):
    #Generate a N bit size binary array 
    for i in range(network_size*network_size):
        binary_array.append(str(bin(i)[2:]))

    #Make every element of the array have the same lenght by inserting zeroes in front of it  
    for i in range(network_size*network_size):
        binary_array[i]=binary_array[i].zfill(len(binary_array[network_size*network_size-1]))

def bit_reversal(binary_array,datapath_binary_array):
    for i in range(network_size*network_size):
        datapath_binary_array.append(binary_array[i][::-1])

def perfect_shuffle(binary_array,datapath_binary_array):
    for i in range(network_size*network_size):
        shuffle=binary_array[i]
        shuffle=shuffle[1:]+shuffle[0:1]
        datapath_binary_array.append(shuffle)

def butterfly(binary_array,datapath_binary_array):
    for i in range(network_size*network_size):
        butterfly=binary_array[i]
        butterfly_begin=butterfly[0]
        butterfly_last=butterfly[-1]
        datapath_binary_array.append(butterfly_last+butterfly[1:-1]+butterfly_begin)

def matrix_transpose(binary_array,datapath_binary_array):
    rotate=round(network_size/2)
    for i in range(network_size*network_size):
        matrix_transpose=binary_array[i]
        matrix_transpose=matrix_transpose[rotate:]+matrix_transpose[0:rotate]
        datapath_binary_array.append(matrix_transpose)

def complement(binary_array,datapath_binary_array):
        complement=binary_array[::-1]
        for i in range(network_size*network_size):
            datapath_binary_array.append(complement[i])

def user_input(binary_array,datapath_binary_array):
    print('(0)Bit reversal')
    print('(1)Perfect shuffle')
    print('(2)Butterfly')
    print('(3)Matrix Transpose')
    print('(4)Complement')
    datapath=int(input())
    if(datapath==0):
        bit_reversal(binary_array,datapath_binary_array)
    if(datapath==1):
        perfect_shuffle(binary_array,datapath_binary_array)
    if(datapath==2):
        butterfly(binary_array,datapath_binary_array)
    if(datapath==3):
        matrix_transpose(binary_array,datapath_binary_array)
    if(datapath==4):
        complement(binary_array,datapath_binary_array)

def add_edges(G,binary_array,datapath_binary_array):
    half = len(binary_array[0])//2
    for i in range(network_size*network_size):
        
        sender=str(int((binary_array[i][:half]),2))+str(int((binary_array[i][half:]),2))
        sender_X=int(sender[:len(sender)//2])
        sender_Y=int(sender[len(sender)//2:])
        
        recipient=str(int((datapath_binary_array[i][half:]),2))+str(int((datapath_binary_array[i][:half]),2))
        recipient_X=int(recipient[:len(recipient)//2])
        recipient_Y=int(recipient[len(recipient)//2:])

        print(sender,recipient)
        G.add_edge((sender_X, sender_Y),(recipient_Y ,recipient_X ))

if __name__ == "__main__":
    binary_array=[]
    datapath_binary_array=[]
    generate_binary_network(binary_array)
     
    user_input(binary_array,datapath_binary_array)

    G = nx.grid_2d_graph(network_size,network_size)
    G = nx.create_empty_copy(G,with_data=True)
    G = nx.DiGraph(G)
    pos = {(x,y):(x,y) for x,y in G.nodes()}
    
    add_edges(G,binary_array,datapath_binary_array)

    plt.clf()
    nx.draw(G, pos=pos, 
        with_labels=True,
        node_size=2400,
        node_shape="s"
        ,connectionstyle="arc3,rad=0.4")
    plt.show()

