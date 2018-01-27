#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "asennima"
__date__ = "$May 3, 2016 8:02:27 PM$"

import os
import sys
import time
import shutil
import traceback
import distutils
from subprocess import Popen
import struct
import array
import glob
from subprocess import Popen

def _writeNewFileWithSwapping(fin, fout, startPosition):
    fin.seek(startPosition)
    while True:
        header_found = False
        bytes = fin.read(2)
        if len(bytes) != 2 or bytes == '':
            break #end of file
        bytes, = struct.unpack(">H", bytes)
        if bytes == 0x770b:
            header_found = True
            frame_size = fin.read(2)
            if frame_size == '':
                break #end of file
            frame_size, = struct.unpack('<H',frame_size)
            frame_size = (frame_size+1) * 2
            fin.seek(-4,1)
            string_read = fin.read(frame_size)
            if len(string_read) == frame_size:
                arr = array.array('H', string_read)
                arr.byteswap()
                string_read = arr.tostring()
                fout.write(string_read)
            else:
                break
        else:
            fin.seek(-1,1)
            
def parseEsCleanerMain(inputfile=None, outputfile=None):        
    try:        
        if inputfile == '' or outputfile == '' or inputfile == None or outputfile == None:
            raise Exception('Filename(s) specified are invalid')
        fin = open(inputfile,"rb")
        fout = open(outputfile,"wb")
        while True:
            header_found = False
            bytes = fin.read(2)
            if len(bytes) != 2 or bytes == '':
                break #end of file
            bytes, = struct.unpack(">H", bytes)
            if bytes == 0xb77:
                print "Header found. Proceeding without swapping"
                _writeNewFileWithoutSwapping(fin, fout, fin.tell()-2)
            elif bytes == 0x770b:
                print "Header found. Proceeding with swapping"
                _writeNewFileWithSwapping(fin, fout, fin.tell()-2)
            else:
                fin.seek(-1,1)
        fin.close()
        fout.close()

    except Exception as e:
        print "error({0}): {1}".format(e.errno, e.strerror)
        raise e

if __name__ == "__main__":
    print "ES Parse Cleaner"
    input_mydir = 'C:\\HATSFramework\\HATS\\bin\\Dolby\\RefDec v0.70\\'
    output_mydir = 'C:\\HATSFramework\\HATS\\bin\\Dolby\\RefDec v0.70\\ElementaryStreams\\'
    #final_mydir = 'C:\\DolbyCertification\\ES\\System\\BitstreamPassThrough\\ByteSwapped\\ByteCopied\\'
    count = 0
    '''for file in os.listdir(input_mydir):
        if not file.endswith(".txt"):
            print("Converting %s"%(input_mydir+file))
            if file != "ByteSwapped" and file != "TextFiles" and file != "NotByteSwapped":
                parseEsCleanerMain((input_mydir+file),(output_mydir+file))
                count = count + 1
                print count
            #time.sleep(2)'''

    #file = '2ch_typical.ec3'
    '''for file in os.listdir(output_mydir):
        with open("final_mydir+file","a") as myfile:
            myfile.write()'''
    for file in os.listdir(input_mydir):
        if os.path.splitext(file)[1] == ".trp":
            extract_cmd = 'RefDec.exe ' + '-if "' + file + '" -ext -pid1 64'            
            tool_process = Popen(extract_cmd)
            tool_process.communicate()
            output_file_url = os.path.join(os.getcwd(), 'elementary_PID_64.es')
            target_file_url = os.path.join(output_mydir, os.path.splitext(os.path.split(file)[-1])[0]) + '.es'
            if os.path.exists(output_file_url):
                if os.path.exists(target_file_url):
                    os.remove(target_file_url)
                os.rename(output_file_url, target_file_url)
                
                
                
            '''with open((output_mydir+file),'ab') as fo:
                with open((input_mydir+file),'rb') as fi:
                    print((final_mydir+file)+"-copied from-"+(output_mydir+file))
                    fo.write(3 * fi.read())
                    #fo.write(fi.read())
                    #fo.write(fi.read())
                    count = count + 1
                    print count'''
            

        
    
    
