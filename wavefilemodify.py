# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "asennima"
__date__ = "$Nov 23, 2015 3:26:15 PM$"

import wave
import struct

if __name__ == "__main__":
    
    ip_filename = "C:\\Users\\asennima\\Desktop\\G3P1_03.wav"
    op_filename = "C:\\Users\\asennima\\Desktop\\G3P1_03_simulated.wav"
    fin = open(ip_filename,'rb')
    fread = fin.read(44)
    fin.close()
    fout = open(op_filename,'wb')
    fout.write(fread)
    fout.close()

    fout = open(op_filename,'ab')
    wrd=wave.open("C:\\Users\\asennima\\Desktop\\G3P1_03_simulated.wav","r")
    for x in wrd:
        print x
    fout.close()
    
    
    
