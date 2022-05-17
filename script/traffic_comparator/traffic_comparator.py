from os import listdir
import os
from os.path import isfile, join
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QCheckBox
#from PyQt5 import Qtcore
import sys

logs_1 = [f for f in listdir("MOORE-MOORE-MOORE") if isfile(join("MOORE-MOORE-MOORE", f))]

global lenght
plot_1=[]
plot_2=[]
plot_3=[]
plot_4=[]
plot_5=[]
plot_6=[]
plot_7=[]
plot_8=[]

def file_open(x,y):
    logs_1_path="MOORE-MOORE-MOORE/tb_router_"+str(x)+str(y)+".log"
    logs_2_path="MOORE-MOORE-MEALY/tb_router_"+str(x)+str(y)+".log"
    logs_3_path="MOORE-MEALY-MOORE/tb_router_"+str(x)+str(y)+".log"
    logs_4_path="MOORE-MEALY-MEALY/tb_router_"+str(x)+str(y)+".log"
    logs_5_path="MEALY-MEALY-MEALY/tb_router_"+str(x)+str(y)+".log"
    logs_6_path="MEALY-MEALY-MOORE/tb_router_"+str(x)+str(y)+".log"
    logs_7_path="MEALY-MOORE-MOORE/tb_router_"+str(x)+str(y)+".log"
    logs_8_path="MEALY-MOORE-MEALY/tb_router_"+str(x)+str(y)+".log"

    log_1=open(logs_1_path,"r") 
    log_2=open(logs_2_path,"r")
    log_3=open(logs_3_path,"r")
    log_4=open(logs_4_path,"r")
    log_5=open(logs_5_path,"r")
    log_6=open(logs_6_path,"r")
    log_7=open(logs_7_path,"r")
    log_8=open(logs_8_path,"r")

    log_1_line_read=log_1.readlines() 
    log_2_line_read=log_2.readlines()
    log_3_line_read=log_3.readlines()
    log_4_line_read=log_4.readlines()
    log_5_line_read=log_5.readlines()
    log_6_line_read=log_6.readlines()
    log_7_line_read=log_7.readlines()
    log_8_line_read=log_8.readlines()
    
    return log_1_line_read,log_2_line_read,log_3_line_read,log_4_line_read,log_5_line_read,log_6_line_read,log_7_line_read,log_8_line_read

def data_filter():   
    number_of_logs=len(logs_1)

    for x in range(int(number_of_logs/4)):
        for y in range(int(number_of_logs/4)):
            
            log_line_read=file_open(x,y)
            
            for i in range(len(log_line_read[0])):
                value1=log_line_read[0][i][34:]
                value2=log_line_read[1][i][34:]
                value3=log_line_read[2][i][34:]
                value4=log_line_read[3][i][34:]
                value5=log_line_read[4][i][34:]
                value6=log_line_read[5][i][34:]
                value7=log_line_read[6][i][34:]
                value8=log_line_read[7][i][34:]
                value1=int(value1[:-3])
                value2=int(value2[:-3])
                value3=int(value3[:-3])
                value4=int(value4[:-3])
                value5=int(value5[:-3])
                value6=int(value6[:-3])
                value7=int(value7[:-3])
                value8=int(value8[:-3])
                plot_1.append(value1)
                plot_2.append(value2)
                plot_3.append(value3)
                plot_4.append(value4)
                plot_5.append(value5)
                plot_6.append(value6)
                plot_7.append(value7)
                plot_8.append(value8)
    
    return (len(log_line_read[0]))

def graph():
    font1 = {'family':'serif','color':'blue','size':30}
    font2 = {'family':'serif','color':'darkred','size':30}
    plt.title("Troughput test", fontdict = font1)
    plt.xlabel("Time",fontdict = font2)
    plt.ylabel("Flit",fontdict = font2)
    plt.grid()
    plt.draw()
    plt.show()

def gen_pos(pos):     
    for i in range(lenght):
        pos.append(i)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi("gui_source/traffic_comparator.ui", self) # Load the .ui file
        self.show() # Show the GUI
        #Push button
        self.QPushButton = self.findChild(QtWidgets.QPushButton, "pushButton_1")
        self.pushButton_1.clicked.connect(self.pressedQPushButton_1)
        self.QPushButton = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.pushButton_2.clicked.connect(self.pressedQPushButton_2)
        #Checkboxes
        self.checkBox_1.stateChanged.connect(self.selected_plot_1)
        self.checkBox_2.stateChanged.connect(self.selected_plot_2)
        self.checkBox_3.stateChanged.connect(self.selected_plot_3)
        self.checkBox_4.stateChanged.connect(self.selected_plot_4)
        self.checkBox_5.stateChanged.connect(self.selected_plot_5)
        self.checkBox_6.stateChanged.connect(self.selected_plot_6)
        self.checkBox_7.stateChanged.connect(self.selected_plot_7)
        self.checkBox_8.stateChanged.connect(self.selected_plot_8)
        
        #User inputs
        self.lineEdit_1 = self.findChild(QtWidgets.QLineEdit, "lineEdit_1")
        self.lineEdit_2 = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.lineEdit_3 = self.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.lineEdit_4 = self.findChild(QtWidgets.QLineEdit, "lineEdit_4")
        self.lineEdit_5 = self.findChild(QtWidgets.QLineEdit, "lineEdit_5")
        self.lineEdit_6 = self.findChild(QtWidgets.QLineEdit, "lineEdit_6")
        self.lineEdit_7 = self.findChild(QtWidgets.QLineEdit, "lineEdit_7")
        self.lineEdit_8 = self.findChild(QtWidgets.QLineEdit, "lineEdit_8")

    def selected_plot_1(self):
        global lenght
        if self.checkBox_1.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_1[:lenght]),pos,color="aquamarine")#MOORE-MOORE-MOORE
            graph()
        else:
            line1.remove()
            

    def selected_plot_2(self):
        global lenght
        if self.checkBox_2.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_2[:lenght]),pos,color="blue")      #MOORE-MOORE-MEALY
            graph()

    def selected_plot_3(self):
        global lenght
        if self.checkBox_3.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_3[:lenght]),pos,color="lime")      #MOORE-MEALY-MOORE
            graph()

    def selected_plot_4(self):
        global lenght
        if self.checkBox_4.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_4[:lenght]),pos,color="indigo")    #MOORE-MEALY-MEALY
            graph()

    def selected_plot_5(self):
        global lenght
        if self.checkBox_5.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_5[:lenght]),pos,color="red")       #MEALY-MEALY-MEALY
            graph()

    def selected_plot_6(self):
        global lenght
        if self.checkBox_6.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_6[:lenght]),pos,color="chocolate") #MEALY-MEALY-MOORE
            graph()
  
    def selected_plot_7(self):
        global lenght
        if self.checkBox_7.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_7[:lenght]),pos,color="peru")      #MEALY-MOORE-MOORE
            graph()

    def selected_plot_8(self):
        global lenght
        if self.checkBox_3.isChecked() == True:
            pos=[]
            gen_pos(pos)
            plt.plot((plot_8[:lenght]),pos,color="tomato")    #MEALY-MOORE-MEALY
            graph()

    def pressedQPushButton_1(self):
        graph()

    def pressedQPushButton_2(self):
        plt.clf()
      
if __name__ == "__main__":
    global lenght
    lenght=data_filter()
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
