# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "asennima"
__date__ = "$Jan 25, 2016 5:34:46 PM$"
__email__="arulmani.sennimalai@harmonicinc.com"

import struct
import sys
import array
import getopt
import os
import csv
import itertools
import glob
import wave
import subprocess
import time
import math

def compareCSVfiles_freqTools(file1,file2,chan_no):

    input_file = file1
    output_file = file2

    result_file = os.path.splitext(os.path.commonprefix([input_file,output_file]))[0] + "result" + "_" + str(chan_no) + ".csv"
    result_header = ["Frquency(Hz)","Ip_Ampt(dBFS)","Op_Ampt(dBFS)","Amplitde_Diff","Result"]
    
    with open(input_file) as csvfile1:
        with open(output_file) as csvfile2:
            with open(result_file,'w') as csvresultfile:
                reader1 = csv.reader(csvfile1,delimiter='\t')
                reader2 = csv.reader(csvfile2,delimiter='\t')
                writer = csv.writer(csvresultfile,delimiter=',',lineterminator='\n')
                writer.writerow(result_header)
                for lhs, rhs in itertools.izip(reader1, reader2):                    
                    diff = abs(float(lhs[1])- float(rhs[1]))
                    if diff > 1:
                        result = 'Fail'
                    else:
                        result = 'Pass'
                    result_list = [float(lhs[0].replace(",","")),float(lhs[1]), float(rhs[1]), diff, result]
                    writer.writerow(result_list)
                    
        '''with open(input_file) as csvfile1:
        with open(output_file) as csvfile2:
            reader1 = csv.reader(csvfile1,delimiter='\t')
            reader2 = csv.reader(csvfile2,delimiter='\t')
            for row1 in reader1:
                print float(row1[0].replace(",","")),float(row2[0].replace(",",""))
                print float(row1[1]),float(row2[1])
            #print(row['A'], row['B'])'''
            
def compareCSVfiles_timeTools(file1,file2,chan_no):

    input_file = file1
    output_file = file2

    result_file = os.path.splitext(os.path.commonprefix([input_file,output_file]))[0] + "result" + "_" + str(chan_no) + ".csv"
    result_header = ["Time(S)","Ip_Ampt(dBFS)","Op_Ampt(dBFS)","Amplitde_Diff","Result"]
    
    with open(input_file) as csvfile1:
        with open(output_file) as csvfile2:
            with open(result_file,'w') as csvresultfile:
                reader1 = csv.reader(csvfile1,delimiter='\t')
                reader2 = csv.reader(csvfile2,delimiter='\t')
                writer = csv.writer(csvresultfile,delimiter=',',lineterminator='\n')
                writer.writerow(result_header)
                for lhs, rhs in itertools.izip(reader1, reader2):
                    #if lhs[0] == rhs[0]:
                    diff = abs(float(lhs[1])- float(rhs[1]))
                    if diff > 1:
                        result = 'Fail'
                    else:
                        result = 'Pass'
                    result_list = [float(lhs[0].replace(",","")),float(lhs[1]), float(rhs[1]), diff, result]
                    writer.writerow(result_list)
                    
        '''with open(input_file) as csvfile1:
        with open(output_file) as csvfile2:
            reader1 = csv.reader(csvfile1,delimiter='\t')
            reader2 = csv.reader(csvfile2,delimiter='\t')
            for row1 in reader1:
                print float(row1[0].replace(",","")),float(row2[0].replace(",",""))
                print float(row1[1]),float(row2[1])
            #print(row['A'], row['B'])'''
    

def op_validation_ampVstime(input_file,output_file):
    NumberofChan_input = 0
    NumberofChan_output = 0
    
    destination_folder = "C:\\AudioTest-API\\Python_Results_Files\\AmpVsTime\\"
            
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"rb")
    
    print input_file, output_file
        
    fin.read(22)
    fout.read(22)
    
    NumChannelsString=fin.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString != '':
        NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
        print("NumChannels in input=",NumChannels[0])
        NumberofChan_input = int(NumChannels[0])
    else:
        print "No data available to read"
        sys.exit(2)

    NumChannelsString1=fout.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString1 != '':
        NumChannels1=struct.unpack("H",NumChannelsString1) # 'H' unsigned 16-bit integer
        print("NumChannels in output=",NumChannels1[0])
        NumberofChan_output = int(NumChannels1[0])
    else:
        print "No data available to read"
        sys.exit(2)
    
    '''for x in range(0,(NumberofChan_input)):
        filename = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        cmd = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename
        #os.system(cmd)'''

    for x in range(0,(NumberofChan_output)):
        filename_ip = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        filename_op = os.path.splitext(os.path.basename(output_file))[0] + '_' + str(x) + '.csv'
        cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\amp_vs_time.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename_ip
        cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\amp_vs_time.exe\" -c"+str(x)+" -t "+output_file + ">" + destination_folder + filename_op
        os.system(cmd_ip)
        os.system(cmd_op)
        time.sleep(2)
        result_ip_file = (destination_folder + filename_ip)
        result_op_file = (destination_folder + filename_op)
        '''try:
            result_ip_file = (destination_folder + filename_ip)
            result_op_file = (destination_folder + filename_op)
            print result_ip_file, result_op_file
            #fip = open(result_ip_file,'r')
            #fop = open(result_op_file,'r')
            
            #fip.close()
            #fop.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)'''
            
        compareCSVfiles_timeTools(result_ip_file,result_op_file,x)
            
        #fip = open(destination_folder + filename_ip,'w')
        #fop = open(destination_folder + filename_op,'w')
        #cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file
        #cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+output_file
        #subprocess.call(cmd_ip,stdout = fin)
        #subprocess.call(cmd_op,stdout = fop)
        #fip.close()
        #fop.close()
                
    '''with open(destination_folder+"5_frqstp_0.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter='\t')
        for row in reader:
            print float(row[0].replace(",",""))
            print float(row[1])
            #print(row['A'], row['B'])'''
        
    
    fin.close()
    fout.close()

def op_validation_thdVsFreq(input_file,output_file):
    NumberofChan_input = 0
    NumberofChan_output = 0
    
    destination_folder = "C:\\AudioTest-API\\Python_Results_Files\\ThdVsFreq\\"
            
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"rb")
    
    print input_file, output_file
        
    fin.read(22)
    fout.read(22)
    
    NumChannelsString=fin.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString != '':
        NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
        print("NumChannels in input=",NumChannels[0])
        NumberofChan_input = int(NumChannels[0])
    else:
        print "No data available to read"
        sys.exit(2)

    NumChannelsString1=fout.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString1 != '':
        NumChannels1=struct.unpack("H",NumChannelsString1) # 'H' unsigned 16-bit integer
        print("NumChannels in output=",NumChannels1[0])
        NumberofChan_output = int(NumChannels1[0])
    else:
        print "No data available to read"
        sys.exit(2)
    
    '''for x in range(0,(NumberofChan_input)):
        filename = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        cmd = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename
        #os.system(cmd)'''

    for x in range(0,(NumberofChan_output)):
        filename_ip = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        filename_op = os.path.splitext(os.path.basename(output_file))[0] + '_' + str(x) + '.csv'
        cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\thd_vs_freq.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename_ip
        cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\thd_vs_freq.exe\" -c"+str(x)+" -t "+output_file + ">" + destination_folder + filename_op
        os.system(cmd_ip)
        os.system(cmd_op)
        time.sleep(2)
        result_ip_file = (destination_folder + filename_ip)
        result_op_file = (destination_folder + filename_op)
        '''try:
            result_ip_file = (destination_folder + filename_ip)
            result_op_file = (destination_folder + filename_op)
            print result_ip_file, result_op_file
            #fip = open(result_ip_file,'r')
            #fop = open(result_op_file,'r')
            
            #fip.close()
            #fop.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)'''
            
        compareCSVfiles_freqTools(result_ip_file,result_op_file,x)
            
        #fip = open(destination_folder + filename_ip,'w')
        #fop = open(destination_folder + filename_op,'w')
        #cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file
        #cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+output_file
        #subprocess.call(cmd_ip,stdout = fin)
        #subprocess.call(cmd_op,stdout = fop)
        #fip.close()
        #fop.close()
                
    '''with open(destination_folder+"5_frqstp_0.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter='\t')
        for row in reader:
            print float(row[0].replace(",",""))
            print float(row[1])
            #print(row['A'], row['B'])'''
        
    
    fin.close()
    fout.close()
    
def op_validation_freqresp(input_file,output_file):
    
    NumberofChan_input = 0
    NumberofChan_output = 0
    
    destination_folder = "C:\\AudioTest-API\\Python_Results_Files\\FreqResp\\"
            
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"rb")
    
    print input_file, output_file
        
    fin.read(22)
    fout.read(22)
    
    NumChannelsString=fin.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString != '':
        NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
        print("NumChannels in input=",NumChannels[0])
        NumberofChan_input = int(NumChannels[0])
    else:
        print "No data available to read"
        sys.exit(2)

    NumChannelsString1=fout.read(2) # Should be 1 for mono, 2 for stereo
    if NumChannelsString1 != '':
        NumChannels1=struct.unpack("H",NumChannelsString1) # 'H' unsigned 16-bit integer
        print("NumChannels in output=",NumChannels1[0])
        NumberofChan_output = int(NumChannels1[0])
    else:
        print "No data available to read"
        sys.exit(2)
    
    '''for x in range(0,(NumberofChan_input)):
        filename = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        cmd = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename
        #os.system(cmd)'''

    for x in range(0,(NumberofChan_output)):
        filename_ip = os.path.splitext(os.path.basename(input_file))[0] + '_' + str(x) + '.csv'
        filename_op = os.path.splitext(os.path.basename(output_file))[0] + '_' + str(x) + '.csv'
        cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file + ">" + destination_folder + filename_ip
        cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+output_file + ">" + destination_folder + filename_op
        os.system(cmd_ip)
        os.system(cmd_op)
        time.sleep(2)
        result_ip_file = (destination_folder + filename_ip)
        result_op_file = (destination_folder + filename_op)
        '''try:
            result_ip_file = (destination_folder + filename_ip)
            result_op_file = (destination_folder + filename_op)
            print result_ip_file, result_op_file
            #fip = open(result_ip_file,'r')
            #fop = open(result_op_file,'r')
            
            #fip.close()
            #fop.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)'''
            
        compareCSVfiles_freqTools(result_ip_file,result_op_file,x)
            
        #fip = open(destination_folder + filename_ip,'w')
        #fop = open(destination_folder + filename_op,'w')
        #cmd_ip = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+input_file
        #cmd_op = "\"C:\\Dolby Laboratories\\Software Audio Test Suite 2.5\\tools\\freq_resp.exe\" -c"+str(x)+" -t "+output_file
        #subprocess.call(cmd_ip,stdout = fin)
        #subprocess.call(cmd_op,stdout = fop)
        #fip.close()
        #fop.close()
                
    '''with open(destination_folder+"5_frqstp_0.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter='\t')
        for row in reader:
            print float(row[0].replace(",",""))
            print float(row[1])
            #print(row['A'], row['B'])'''
        
    
    fin.close()
    fout.close()
        
def convertTXTtoCSV():
    
    ip_directory = "C:\\AudioTest-API\\DolbyTools_Results"
    op_directory = "C:\\AudioTest-API\\DolbyTools_Results\\txtTOcsv_coverted"
    
    txt_files = os.path.join(ip_directory, '*.txt')

    for txt_file in glob.glob(txt_files):
        with open(txt_file, "rb") as input_file:
            in_txt = csv.reader(input_file, delimiter=',')
            filename = os.path.splitext(os.path.basename(txt_file))[0] + '.csv'

            with open(os.path.join(op_directory, filename), 'wb+') as output_file:
                out_csv = csv.writer(output_file)
                out_csv.writerows(in_txt)
            
    
if __name__ == "__main__":

    try:
        inputfile = ''
        outputfile = ''
        opValidationOption = 255
        try:
            opts, args = getopt.getopt(sys.argv[1:],"hi:o:x:",["ifile=","ofile=","xoption="])
        except getopt.GetoptError:
            print 'Usage error.'
            print 'Usage: ' + sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-freqresp_validation,2-ampVstimeValidation,3-thdVsFreqValidation> '
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-freqresp_validation,2-ampVstimeValidation,3-thdVsFreqValidation> '
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = os.path.abspath(arg)
            elif opt in ("-o", "--ofile"):
                outputfile = os.path.abspath(arg)
            elif opt in ("-x", "--xoption"):
                opValidationOption = arg
                                
        if inputfile == '' or outputfile == '' or opValidationOption == '':
            print 'Usage error.'
            print 'Usage: ' + sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-freqresp_validation,2-ampVstimeValidation,3-thdVsFreqValidation> '
            sys.exit()
            
        ip_filename, ip_file_extension = os.path.splitext(inputfile)
        op_filename, op_file_extension = os.path.splitext(outputfile)
    
        if ip_file_extension != '.wav' or op_file_extension != '.wav':
            print "wrong file format - Input file format must be .wav"    
    
        if opValidationOption == '1':
            op_validation_freqresp(inputfile,outputfile)
        elif opValidationOption == '2':
            op_validation_ampVstime(inputfile,outputfile)
        elif opValidationOption == '3':
            op_validation_thdVsFreq(inputfile,outputfile)
        else:
            print "Invalid option - Use Help for valid options"

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)  
   
    
