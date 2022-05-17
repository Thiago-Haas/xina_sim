#Python script for header generation on a XY routing NOC and traffic generation

def user_input():
    print("(0)Bit reversal")
    print("(1)Perfect shuffle")
    print("(2)Butterfly")
    print("(3)Matrix Transpose")
    print("(4)Complement")
    global datapath
    datapath=int(input())
    #print("Size of network:") for testing purposes network was locked at 4x4
    global x_range
    x_range=4
    print("Number of packets that will be tested:")
    global n_packets
    n_packets=int(input())
    print("Number of flits per packet")
    global n_flits
    n_flits=int(input())

def binary_array_generator(binary_array):

    for i in range(x_range*x_range):#Generate a N bit size binary array 
        binary_array.append(str(bin(i)[2:]))
 
    for i in range(x_range*x_range):#Make every element of the array have the same lenght by inserting zeroes in front of it
        binary_array[i]=binary_array[i].zfill(len(binary_array[x_range*x_range-1]))

def datapath_selection(datapath,binary_array,datapath_binary_array):
    if(datapath==0):#Bit reversal
        for i in range(x_range*x_range):
            datapath_binary_array.append(binary_array[i][::-1])
    
    elif(datapath==1):#Perfect shuffle
        for i in range(x_range*x_range):
            shuffle=binary_array[i]
            shuffle=shuffle[1:]+shuffle[0:1]
            datapath_binary_array.append(shuffle)

    elif(datapath==2):#Butterfly
        for i in range(x_range*x_range):
            butterfly=binary_array[i]
            butterfly_begin=butterfly[0]
            butterfly_last=butterfly[-1]
            datapath_binary_array.append(butterfly_last+butterfly[1:-1]+butterfly_begin)

    elif(datapath==3):#Matrix transpose      
        rotate=round(x_range/2)
        for i in range(x_range*x_range):
            matrix_transpose=binary_array[i]
            matrix_transpose=matrix_transpose[rotate:]+matrix_transpose[0:rotate]
            datapath_binary_array.append(matrix_transpose)

    elif(datapath==4):
            complement=binary_array[::-1]#Complement
            for i in range(x_range*x_range):
                datapath_binary_array.append(complement[i])
    else:
        print("Wrong value, program will terminate")#Terminates the program if user inserts wrong input
        exit()
    
    datapath_binary_array_X=[]
    datapath_binary_array_Y=[]
    
    for i in range(x_range*x_range):#String work to set desired header format
            temp=int((len(binary_array[i]))/2)
            datapath_binary_array_X.append(datapath_binary_array[i][:temp])
            datapath_binary_array_Y.append(datapath_binary_array[i][temp:])
            datapath_binary_array[i]=datapath_binary_array_X[i].zfill(16)+datapath_binary_array_Y[i].zfill(16)

def router_indexes(router_x,router_y):
    for i in range(x_range):#generates routers indexes
        for j in range(x_range):
            router_x.append(i)
            router_y.append(j)

def seed_generator(bSeed,sbSeed,router_x,router_y):
    seedx=[]
    seedy=[]
    for i in range(x_range**2):#seed generator
        seedx.append(abs((x_range*((router_x[i]*x_range)+router_y[i]))+(2**((router_x[i])+8))))
        seedx[i]=bin(seedx[i])[2:].zfill(16)

        seedy.append(abs((x_range*((router_y[i]*x_range)+router_x[i]))+(2**((router_y[i])+8))))
        seedy[i]=bin(seedy[i])[2:].zfill(16)

        bSeed.append(seedx[i]+seedy[i])

        sbSeed.append(seedx[i]+seedy[i])

def LFSR(x):
    result=[]
    for i in range(x_range**2):#XOR
        
        xor=((ord(x[i][0])^ord(x[i][10]))^ord(x[i][30]))^ord(x[i][31])
        xor=str(xor)
        
        x[i]=x[i][1:]+x[i][:1]#1 bit left rotation

        temp=list(x[i])#Inserts XOR result at the rightmost bit
        temp[-1]=xor
        temp="".join(temp)
        x[i]=temp

        result.append(x[i])
    return result

def LFSR_call(bSeed,sbSeed,LFSR_result):
    #LFSR call
    LFSR_result.append(sbSeed)
    for i in range(n_packets*n_flits):  
        LFSR_result.append(LFSR(bSeed))

def write_file(x_range,LFSR_result):
    for i in range(x_range**2):#Clears old files
        file_name="../../input_files_tb/tb_input_router_"+str(router_x[i])+str(router_y[i])+".txt"
        file=open(file_name,"w")
        file.close()
    for i in range(x_range**2):#Write new files
        packet_position=0
        for j in range(n_packets):
            flit_position=0
            file_name="../../input_files_tb/tb_input_router_"+str(router_x[i])+str(router_y[i])+".txt"
            file=open(file_name,"a") 
            file.write("1"+datapath_binary_array[i]+"\n")
            while(flit_position<(n_flits-2)):
                file.write("0"+LFSR_result[flit_position+packet_position][i]+"\n")
                flit_position=flit_position+1
            file.write("1"+LFSR_result[flit_position+packet_position][i]+"\n")
            packet_position=packet_position+n_flits-1
        file.close()

if __name__ == "__main__":
    user_input()

    binary_array=[]
    binary_array_generator(binary_array)
    
    datapath_binary_array=[]
    datapath_selection(datapath,binary_array,datapath_binary_array)

    router_x=[]
    router_y=[]
    router_indexes(router_x,router_y)

    bSeed=[]
    sbSeed=[]
    seed_generator(bSeed,sbSeed,router_x,router_y)

    LFSR_result=[]
    LFSR_call(bSeed,sbSeed,LFSR_result)

    write_file(x_range,LFSR_result)
