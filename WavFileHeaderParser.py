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

def headerParser(inputfile):
    
    headerbytes = 0
    fin = open(inputfile,"rb")
    ChunkID=fin.read(4) # First four bytes are ChunkID which must be "RIFF" in ASCII
    print("ChunkID=",ChunkID)
    headerbytes = headerbytes + 4
    
    ChunkSizeString=fin.read(4) # Total Size of File in Bytes - 8 Bytes
    ChunkSize=struct.unpack('I',ChunkSizeString) # 'I' Format is to to treat the 4 bytes as unsigned 32-bit inter
    TotalSize=ChunkSize[0]+8 # The subscript is used because struct unpack returns everything as tuple
    print("TotalSize=",TotalSize)
    headerbytes = headerbytes + 4
    
    DataSize=TotalSize-44 # This is the number of bytes of data
    print("DataSize=",DataSize)
    
    Format=fin.read(4) # "WAVE" in ASCII
    print("Format=",Format)
    headerbytes = headerbytes + 4
    
    SubChunk1ID=fin.read(4) # "fmt " in ASCII
    print("SubChunk1ID=",SubChunk1ID)
    headerbytes = headerbytes + 4
    
    SubChunk1SizeString=fin.read(4) # Should be 16 (PCM, Pulse Code Modulation)
    SubChunk1Size=struct.unpack("I",SubChunk1SizeString) # 'I' format to treat as unsigned 32-bit integer
    print("SubChunk1Size=",SubChunk1Size[0])
    headerbytes = headerbytes + 4
    
    AudioFormatString=fin.read(2) # Should be 1 (PCM)
    AudioFormat=struct.unpack("H",AudioFormatString) # 'H' format to treat as unsigned 16-bit integer
    print("AudioFormat=",AudioFormat[0])
    headerbytes = headerbytes + 2
    
    NumChannelsString=fin.read(2) # Should be 1 for mono, 2 for stereo
    NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
    print("NumChannels=",NumChannels[0])
    headerbytes = headerbytes + 2
    
    SampleRateString=fin.read(4) # Should be 44100 (CD sampling rate)
    SampleRate=struct.unpack("I",SampleRateString)
    print("SampleRate=",SampleRate[0])
    headerbytes = headerbytes + 4
    
    ByteRateString=fin.read(4) # 44100*NumChan*2 (88200 - Mono, 176400 - Stereo)
    ByteRate=struct.unpack("I",ByteRateString) # 'I' unsigned 32 bit integer
    print("ByteRate=",ByteRate[0])
    headerbytes = headerbytes + 4
    
    BlockAlignString=fin.read(2) # NumChan*2 (2 - Mono, 4 - Stereo)
    BlockAlign=struct.unpack("H",BlockAlignString) # 'H' unsigned 16-bit integer
    print("BlockAlign=",BlockAlign[0])
    headerbytes = headerbytes + 2
    
    BitsPerSampleString=fin.read(2) # 16 (CD has 16-bits per sample for each channel)
    BitsPerSample=struct.unpack("H",BitsPerSampleString) # 'H' unsigned 16-bit integer
    print("BitsPerSample=",BitsPerSample[0])
    headerbytes = headerbytes + 2
    
    SubChunk2ID=fin.read(4) # "data" in ASCII
    print("SubChunk2ID=",SubChunk2ID)
    headerbytes = headerbytes + 4
    
    SubChunk2SizeString=fin.read(4) # Number of Data Bytes, Same as DataSize
    SubChunk2Size=struct.unpack("I",SubChunk2SizeString)
    print("SubChunk2Size=",SubChunk2Size[0])
    headerbytes = headerbytes + 4
    
    print ("Total bytes in header: ",headerbytes)


def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
   except getopt.GetoptError:
      print 'WavFileHeaderParser.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print 'Input file is "', inputfile
   headerParser(inputfile);
   
if __name__ == "__main__":
    main(sys.argv[1:])
    
    
    
    

