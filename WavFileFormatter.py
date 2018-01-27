# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "asennima"
__date__ = "$Nov 20, 2015 5:21:44 PM$"

import struct
import wave
import random
import sys 
import getopt

def wavefilereader():
    # waverdwave.py
    wrd=wave.open("C:\\AudioTest-API\\5_frqstp.wav","r")
    S1String=wrd.readframes(1) # First Sample
    S1=struct.unpack('i',S1String)
    print("S1=",S1[0])
    S2String=wrd.readframes(1) # Second Sample
    S2=struct.unpack('i',S2String)
    print("S2=",S2[0])
    S3String=wrd.readframes(1) # Third Sample
    S3=struct.unpack('i',S3String)
    print("S3=",S3[0])
    S4String=wrd.readframes(1) # Fourth Sample
    S4=struct.unpack('i',S4String)
    print("S4=",S4[0])
    S5String=wrd.readframes(1) # Fifth Sample
    S5=struct.unpack('i',S5String)
    print("S5=",S5[0])


if __name__ == "__main__":
    
    #wavefilereader()

    # waverd.py
    # When reading a binary file, Python converts values to strings.
    # To decode the strings we need the struct module  
    
    headerbytes = 0
    # open(fname,mode) is the Python way of reading files
    fin = open("C:\\AudioTest-API\\5_frqstp.wav","rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open("C:\\AudioTest-API\\5_frqstp_stephen.wav","wb")
    ChunkID=fin.read(4) # First four bytes are ChunkID which must be "RIFF" in ASCII
    print("ChunkID=",ChunkID)
    headerbytes = headerbytes + 4
    fout.write(ChunkID)
    
    ChunkSizeString=fin.read(4) # Total Size of File in Bytes - 8 Bytes
    ChunkSize=struct.unpack('I',ChunkSizeString) # 'I' Format is to to treat the 4 bytes as unsigned 32-bit inter
    TotalSize=ChunkSize[0]+8 # The subscript is used because struct unpack returns everything as tuple
    print("TotalSize=",TotalSize)
    headerbytes = headerbytes + 4
    fout.write(ChunkSizeString)
    
    DataSize=TotalSize-44 # This is the number of bytes of data
    print("DataSize=",DataSize)
    
    Format=fin.read(4) # "WAVE" in ASCII
    print("Format=",Format)
    headerbytes = headerbytes + 4
    fout.write(Format)
    
    SubChunk1ID=fin.read(4) # "fmt " in ASCII
    print("SubChunk1ID=",SubChunk1ID)
    headerbytes = headerbytes + 4
    fout.write(SubChunk1ID)
    
    SubChunk1SizeString=fin.read(4) # Should be 16 (PCM, Pulse Code Modulation)
    SubChunk1Size=struct.unpack("I",SubChunk1SizeString) # 'I' format to treat as unsigned 32-bit integer
    print("SubChunk1Size=",SubChunk1Size[0])
    headerbytes = headerbytes + 4
    fout.write(SubChunk1SizeString)
    
    AudioFormatString=fin.read(2) # Should be 1 (PCM)
    AudioFormat=struct.unpack("H",AudioFormatString) # 'H' format to treat as unsigned 16-bit integer
    print("AudioFormat=",AudioFormat[0])
    headerbytes = headerbytes + 2
    fout.write(AudioFormatString)
    
    NumChannelsString=fin.read(2) # Should be 1 for mono, 2 for stereo
    NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
    print("NumChannels=",NumChannels[0])
    headerbytes = headerbytes + 2
    fout.write(NumChannelsString)
    
    SampleRateString=fin.read(4) # Should be 44100 (CD sampling rate)
    SampleRate=struct.unpack("I",SampleRateString)
    print("SampleRate=",SampleRate[0])
    headerbytes = headerbytes + 4
    fout.write(SampleRateString)
    
    ByteRateString=fin.read(4) # 44100*NumChan*2 (88200 - Mono, 176400 - Stereo)
    ByteRate=struct.unpack("I",ByteRateString) # 'I' unsigned 32 bit integer
    print("ByteRate=",ByteRate[0])
    headerbytes = headerbytes + 4
    fout.write(ByteRateString)
    
    BlockAlignString=fin.read(2) # NumChan*2 (2 - Mono, 4 - Stereo)
    BlockAlign=struct.unpack("H",BlockAlignString) # 'H' unsigned 16-bit integer
    print("BlockAlign=",BlockAlign[0])
    headerbytes = headerbytes + 2
    fout.write(BlockAlignString)
    
    BitsPerSampleString=fin.read(2) # 16 (CD has 16-bits per sample for each channel)
    BitsPerSample=struct.unpack("H",BitsPerSampleString) # 'H' unsigned 16-bit integer
    print("BitsPerSample=",BitsPerSample[0])
    headerbytes = headerbytes + 2
    fout.write(BitsPerSampleString)
    
    SubChunk2ID=fin.read(4) # "data" in ASCII
    print("SubChunk2ID=",SubChunk2ID)
    headerbytes = headerbytes + 4
    fout.write(SubChunk2ID)
    
    SubChunk2SizeString=fin.read(4) # Number of Data Bytes, Same as DataSize
    SubChunk2Size=struct.unpack("I",SubChunk2SizeString)
    print("SubChunk2Size=",SubChunk2Size[0])
    headerbytes = headerbytes + 4
    fout.write(SubChunk2SizeString)
    
    print ("Total bytes in header: ",headerbytes)
    
    
    #S1String=fin.read(2) # Read first data, number between -32768 and 32767
    #S1=struct.unpack("h",S1String)
    #print("S1=",S1[0])
    #S2String=fin.read(2) # Read second data, number between -32768 and 32767
    #S2=struct.unpack("h",S2String)
    #print("S2=",S2[0])
    #S3String=fin.read(2) # Read second data, number between -32768 and 32767
    #S3=struct.unpack("h",S3String)
    #print("S3=",S3[0])
    #S4String=fin.read(2) # Read second data, number between -32768 and 32767
    #S4=struct.unpack("h",S4String)
    #print("S4=",S4[0])
    #S5String=fin.read(2) # Read second data, number between -32768 and 32767
    #S5=struct.unpack("h",S5String)
    #print("S5=",S5[0])
    count = 0
    for i in range(2927618):
        if(count == 120000):
        #if(1):
            #value = random.randint(-32767, 32767)
            #packed_value = struct.pack('h', value)
            packed_value = 2
            packed_value1 = 1
            count = 0
            for i in range(100):
                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1)

                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value1
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1) 

                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value1
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1) 

                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value1
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1) 

                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value1
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1) 

                stringleft = fin.read(2)
                S1=struct.unpack("h",stringleft)
                packed_value_new = int(S1[0]) * packed_value1
                packed_value_new1 = struct.pack("h",packed_value_new)
                fout.write(packed_value_new1) 
            
            '''stringright = fin.read(2)
            S1=struct.unpack("h",stringright)
            packed_value_new = str(int(S1[0]) * packed_value)
            fout.write(packed_value_new)
            
            stringcenter = fin.read(2)
            S1=struct.unpack("h",stringcenter)
            packed_value_new = str(int(S1[0]) * packed_value)
            fout.write(packed_value_new)
            
            stringLFE = fin.read(2)
            S1=struct.unpack("h",stringLFE)
            packed_value_new = str(int(S1[0]) * packed_value)
            fout.write(packed_value_new)
            
            stringLs = fin.read(2)
            S1=struct.unpack("h",stringLs)
            packed_value_new = str(int(S1[0]) * packed_value)
            fout.write(packed_value_new)
            
            stringRs = fin.read(2)
            S1=struct.unpack("h",stringRs)
            packed_value_new = str(int(S1[0]) * packed_value)
            fout.write(packed_value_new)'''
            '''stringright = fin.read(2)
            fout.write(stringright)
            stringcenter = fin.read(2)
            fout.write(stringcenter)
            stringLFE = fin.read(2)
            fout.write(stringLFE)
            stringLs = fin.read(2)
            fout.write(stringLs)
            stringRs = fin.read(2)
            fout.write(stringRs)'''
        else:
            count = count + 12
            stringleft = fin.read(2)
            fout.write(stringleft)
            stringright = fin.read(2)
            fout.write(stringright)
            stringcenter = fin.read(2)
            fout.write(stringcenter)
            stringLFE = fin.read(2)
            fout.write(stringLFE)
            stringLs = fin.read(2)
            fout.write(stringLs)
            stringRs = fin.read(2)
            fout.write(stringRs)
            
    fin.close()
    fout.close()

