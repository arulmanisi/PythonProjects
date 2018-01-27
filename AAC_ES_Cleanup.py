# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

# Program takes Elementary stream(ES) file and performs the cleanup by removing the incomplete frames
# and creates a new ES file

__author__ = "asennima"
__date__ = "$Dec 9, 2015 5:58:46 PM$"
__email__="arulmani.sennimalai@harmonicinc.com"

import struct
import wave
import random
import sys

if __name__ == "__main__":
    
    try:
        #fin = open("C:\\HADAS\\IRP-9444\\captures\\testcase_2_es.aac","rb")
        #fout = open("C:\\HADAS\\IRP-9444\\captures\\testcase_2_es_cleaned.aac","wb")
        fin = open(sys.argv[1],"rb")
        fout = open(sys.argv[2],"wb")
    
        while True:
            #header_found = searchESHeader()
            header_found = False
            byte_1 = fin.read(1)
            if(byte_1 == ''):
                break
            hex_byte_1 = hex(ord(byte_1))
            if int(hex_byte_1,16) == int('0xFF',16):
                byte_2 = fin.read(1)
                if(byte_2 == ''):
                    break
                hex_byte_2 = hex(ord(byte_2))
                if int(hex_byte_2,16) == int('0xF9',16):
                    #print fin.tell()
                    #print hex_byte_1,hex_byte_2
                    header_found = True
                    #print header_found
                    fin.seek(-2,1)
                    #print fin.tell()
                    #break
                else:
                    fin.seek(-1,1)
                
            if header_found:
                if fin.read(2) == '':
                    break
                value = fin.read(2)
                if value == '':
                    break
                #unpack_value = struct.unpack('H',value)
                #string_hex = hex(unpack_value[0])
                #byteswap = ((int(string_hex,16) >> 8) & 0x00FF) | ((int(string_hex,16) << 8) & 0xFF00) 
                #frame_size = ((byteswap & 0x07FF) + 1) * 2
                #print frame_size
                fin.seek(-4,1)
                #string_read = fin.read(frame_size)                
                while True:
                    byte = fin.read(1)
                    #if len(string_read) == frame_size:
                    if not byte:
                        break;
                    fout.write(byte)
                #else:
                #    fin.seek(4,1)
    
        fin.close()
        fout.close()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
