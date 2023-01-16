from PyQt5 import QtWidgets, uic
import networkx as nx
import matplotlib.pyplot as plt
import sys

x_range=4#for testing purposes network was locked at 4x4
data_width=8

def binary_array_generator(binary_array):

    for i in range(x_range*x_range):#Generate a N bit size binary array 
        binary_array.append(str(bin(i)[2:]))
 
    for i in range(x_range*x_range):#Make every element of the array have the same lenght by inserting zeroes in front of it
        binary_array[i]=binary_array[i].zfill(len(binary_array[x_range*x_range-1]))

def bit_reversal(binary_array,datapath_binary_array):
    for i in range(x_range*x_range):
        datapath_binary_array.append(binary_array[i][::-1])

def perfect_shuffle(binary_array,datapath_binary_array):
    for i in range(x_range*x_range):
        shuffle=binary_array[i]
        shuffle=shuffle[1:]+shuffle[0:1]
        datapath_binary_array.append(shuffle)

def butterfly(binary_array,datapath_binary_array):
    for i in range(x_range*x_range):
        butterfly=binary_array[i]
        butterfly_begin=butterfly[0]
        butterfly_last=butterfly[-1]
        datapath_binary_array.append(butterfly_last+butterfly[1:-1]+butterfly_begin)

def matrix_transpose(binary_array,datapath_binary_array):
    rotate=round(x_range/2)
    for i in range(x_range*x_range):
        matrix_transpose=binary_array[i]
        matrix_transpose=matrix_transpose[rotate:]+matrix_transpose[0:rotate]
        datapath_binary_array.append(matrix_transpose)

def complement(binary_array,datapath_binary_array):
        complement=binary_array[::-1]
        for i in range(x_range*x_range):
            datapath_binary_array.append(complement[i])

def datapath_selection(binary_array,datapath_binary_array):
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

def format_datapath(binary_array,datapath_binary_array):
    datapath_binary_array_X=[]
    datapath_binary_array_Y=[]
    if(data_width==32):
        for i in range(x_range*x_range):#String work to set desired header format
                temp=int((len(binary_array[i]))/2)
                datapath_binary_array_X.append(datapath_binary_array[i][:temp])
                datapath_binary_array_Y.append(datapath_binary_array[i][temp:])
                datapath_binary_array[i]=datapath_binary_array_X[i].zfill(16)+datapath_binary_array_Y[i].zfill(16)
    elif(data_width==8):
        for i in range(x_range*x_range):#String work to set desired header format
                temp=int((len(binary_array[i]))/2)
                datapath_binary_array_X.append(datapath_binary_array[i][:temp])
                datapath_binary_array_Y.append(datapath_binary_array[i][temp:])
                datapath_binary_array[i]=datapath_binary_array_X[i].zfill(4)+datapath_binary_array_Y[i].zfill(4)

def router_indexes(router_x,router_y):
    for i in range(x_range):#generates routers indexes
        for j in range(x_range):
            router_x.append(i)
            router_y.append(j)

def seed_generator(bSeed,sbSeed,router_x,router_y):
    seedx=[]
    seedy=[]
    if(data_width==32):
        for i in range(x_range**2):#seed generator
            seedx.append(abs((x_range*((router_x[i]*x_range)+router_y[i]))+(2**((router_x[i])+8))))
            seedx[i]=bin(seedx[i])[2:].zfill(16)

            seedy.append(abs((x_range*((router_y[i]*x_range)+router_x[i]))+(2**((router_y[i])+8))))
            seedy[i]=bin(seedy[i])[2:].zfill(16)

            bSeed.append(seedx[i]+seedy[i])

            sbSeed.append(seedx[i]+seedy[i])
    elif(data_width==8):
        for i in range(x_range**2):#seed generator
            seedx.append(abs(x_range*router_x[i]+router_x[i]+x_range))
            seedx[i]=(bin(seedx[i])[2:].zfill(4))[-4:]
            
            seedy.append(abs(x_range*router_y[i]+router_y[i]+x_range))
            seedy[i]=(bin(seedy[i])[2:].zfill(4))[-4:]

            bSeed.append(seedx[i]+seedy[i])
            print(bSeed[i])

            sbSeed.append((seedx[i]+seedy[i]))

def LFSR(x):
    result=[]
    if(data_width==32):
        for i in range(x_range**2):#XOR

            xor=((ord(x[i][0])^ord(x[i][10]))^ord(x[i][30]))^ord(x[i][31])
            xor=str(xor)

            x[i]=x[i][1:]+x[i][:1]#1 bit left rotation

            temp=list(x[i])#Inserts XOR result at the rightmost bit
            temp[-1]=xor
            temp="".join(temp)
            x[i]=temp

            result.append(x[i])
    elif(data_width==8):
        for i in range(x_range**2):#XOR
            xor=ord(x[i][0])^ord(x[i][2])^ord(x[i][3])^ord(x[i][4])
            xor=str(xor)

            x[i]=x[i][1:]+x[i][:1]#1 bit left rotation

            temp=list(x[i])#Inserts XOR result at the rightmost bit
            temp[-1]=xor
            temp="".join(temp)
            x[i]=temp

            result.append(x[i])

    return result

def LFSR_call(bSeed,sbSeed,LFSR_result,n_packets,n_flits):
    #LFSR call
    LFSR_result.append(sbSeed)
    for i in range(n_packets*n_flits):  
        LFSR_result.append(LFSR(bSeed))

def write_file(x_range,LFSR_result,router_x,router_y,datapath_binary_array,n_packets,n_flits):
    for i in range(x_range**2):#Clears old files
        file_name="../input_files_tb/tb_input_router_"+str(router_x[i])+str(router_y[i])+".txt"
        file=open(file_name,"w")
        file.close()
    for i in range(x_range**2):#Write new files
        packet_position=0
        for j in range(n_packets):
            flit_position=0
            file_name="../input_files_tb/tb_input_router_"+str(router_x[i])+str(router_y[i])+".txt"
            file=open(file_name,"a") 
            file.write("1"+datapath_binary_array[i]+"\n")
            while(flit_position<(n_flits-2)):
                file.write("0"+LFSR_result[flit_position+packet_position][i]+"\n")
                flit_position=flit_position+1
            file.write("1"+LFSR_result[flit_position+packet_position][i]+"\n")
            packet_position=packet_position+n_flits-1
        file.close()

def add_edges(G):
    binary_array=[]
    datapath_binary_array=[]
    binary_array_generator(binary_array)
    datapath_selection(binary_array,datapath_binary_array)

    half = len(binary_array[0])//2
    for i in range(x_range*x_range):    
        sender=str(int((binary_array[i][:half]),2))+str(int((binary_array[i][half:]),2))
        sender_X=int(sender[:len(sender)//2])
        sender_Y=int(sender[len(sender)//2:])
        
        recipient=str(int((datapath_binary_array[i][half:]),2))+str(int((datapath_binary_array[i][:half]),2))
        recipient_X=int(recipient[:len(recipient)//2])
        recipient_Y=int(recipient[len(recipient)//2:])

        G.add_edge((sender_X, sender_Y),(recipient_Y ,recipient_X ))

def generate_graph():
    plt.close()
    G = nx.grid_2d_graph(x_range,x_range)
    G = nx.create_empty_copy(G,with_data=True)
    G = nx.DiGraph(G)
    pos = {(x,y):(x,y) for x,y in G.nodes()}
    
    add_edges(G)

    plt.clf()
    nx.draw(G, pos=pos, 
        with_labels=True,
        node_size=2400,
        node_shape="s"
        ,connectionstyle="arc3,rad=0.4")
    plt.show()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi("gui_source/traffic_generator_gui.ui", self) # Load the .ui file
        self.show() # Show the GUI
                #self.pushButton_2.clicked.connect(self.event_remove_aresta)#Remove aresta
        #Push button
        self.QPushButton = self.findChild(QtWidgets.QPushButton, "pushButton_1")
        self.pushButton_1.clicked.connect(self.pressedQPushButton)
        #Radio buttons
        self.QRadioButton = self.findChild(QtWidgets.QRadioButton, "radioButton_1")
        self.radioButton_1.toggled.connect(self.selected_bit_reversal)
        self.QRadioButton = self.findChild(QtWidgets.QRadioButton, "radioButton_2")
        self.radioButton_2.toggled.connect(self.selected_perfect_shuffle)
        self.QRadioButton = self.findChild(QtWidgets.QRadioButton, "radioButton_3")
        self.radioButton_3.toggled.connect(self.selected_butterfly)
        self.QRadioButton = self.findChild(QtWidgets.QRadioButton, "radioButton_4")
        self.radioButton_4.toggled.connect(self.selected_matrix_transpose)
        self.QRadioButton = self.findChild(QtWidgets.QRadioButton, "radioButton_5")
        self.radioButton_5.toggled.connect(self.selected_complement)
        #User inputs
        self.lineEdit_1 = self.findChild(QtWidgets.QLineEdit, "lineEdit_1")
        self.lineEdit_2 = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")

    def selected_bit_reversal(self,selected):
        if selected:
            global datapath
            datapath=0
            
    def selected_perfect_shuffle(self,selected):
        if selected:
            global datapath
            datapath=1

    def selected_butterfly(self,selected):
        if selected:
            global datapath
            datapath=2

    def selected_matrix_transpose(self,selected):
        if selected:
            global datapath
            datapath=3
    def selected_complement(self,selected):
        if selected:
            global datapath
            datapath=4
            
    def pressedQPushButton(self):
        n_packets=int(self.lineEdit_1.text())
        n_flits=int(self.lineEdit_2.text())

        binary_array=[]
        binary_array_generator(binary_array)

        datapath_binary_array=[]
        datapath_selection(binary_array,datapath_binary_array)
        format_datapath(binary_array,datapath_binary_array)

        router_x=[]
        router_y=[]
        router_indexes(router_x,router_y)

        bSeed=[]
        sbSeed=[]
        seed_generator(bSeed,sbSeed,router_x,router_y)

        LFSR_result=[]
        LFSR_call(bSeed,sbSeed,LFSR_result,n_packets,n_flits)
        
        write_file(x_range,LFSR_result,router_x,router_y,datapath_binary_array,n_packets,n_flits)

        generate_graph()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()