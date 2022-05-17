class bcolors:
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

from os import listdir
import os
from os.path import isfile, join

logs_hw = [f for f in listdir('../log_hw') if isfile(join('../log_hw', f))]
logs_tb = [f for f in listdir('../log_tb') if isfile(join('../log_tb', f))]

def file_check():
    #clears files
    file=open('log_comparison.txt','w')
    file.close()

def compare_logs():
    
    
    number_of_logs=len(logs_hw)

    for x in range(int(number_of_logs/4)):
        for y in range(int(number_of_logs/4)):
            tb_log_path='../log_tb/tb_router_'+str(x)+str(y)+'.log'
            hw_log_path='../log_hw/hw_router_'+str(x)+str(y)+'.log'

            file=open('log_comparison.txt','a')
            if(os.stat(tb_log_path).st_size==0): #If logfile is empty it means that router is in loopback and it can't be read
                print(bcolors.OKBLUE+'LOOPBACK_Router_'+str(x)+str(y)+bcolors.ENDC)
                file.write('LOOPBACK_Router_'+str(x)+str(y)+'\n')
            else:
                tb_log=open(tb_log_path,'r') #reads file
                hw_log=open(hw_log_path,'r')

                tb_line_read=tb_log.readlines() #reads file line
                hw_line_read=hw_log.readlines()


                for i in range(len(hw_line_read)):
                    if(tb_line_read[i]==hw_line_read[i]): #If the lines are equal it means that the logfile is correct
                        print(bcolors.OKGREEN+'OK_Router_'+str(x)+str(y)+'_Flit:'+str(i+1)+bcolors.ENDC)
                        file.write('OK_Router_'+str(x)+str(y)+'_Flit:'+str(i+1)+'\n')
                    else: #If the lines are different it means that the logfile is wrong
                        if(tb_line_read[i].partition(',')[0]!=hw_line_read[i].partition(',')[0]):# Checks if the flit on the logfile is wrong
                            print(bcolors.FAIL+'FAULT_Router_'+str(x)+str(y)+'_Flit:'+str(i+1)+bcolors.ENDC)
                            file.write('FAULT_Router_'+str(x)+str(y)+'_Flit:'+str(i+1)+'\n')
                        else:# if the flit isn't the problem than the timming must be the problem
                            print(bcolors.WARNING+'FAULT_Router_'+str(x)+str(y)+'_Timming:'+str(i+1)+bcolors.ENDC)
                            file.write('FAULT_Router_'+str(x)+str(y)+'_Timming:'+str(i+1)+'\n')

                tb_log.close()
                hw_log.close()
            file.close()

if __name__ == "__main__":
    file_check()
    compare_logs()