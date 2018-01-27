# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "asennima"
__date__ = "$Nov 20, 2015 5:21:44 PM$"

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
import random


def changeChannelAmplitude(input_file,output_file):

    headerbytes = 0
    NumberofChannels = 0
    
    destination_folder = "C:\\AudioTest-API\\Python_SampleModified_Files\\"
    
    output_file = destination_folder + os.path.splitext(os.path.basename(output_file))[0] + ".wav"
    
    # open(fname,mode) is the Python way of reading files
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"wb")
	
    print "Enter the channel no for amplitude scale modification - 0-L,1-R,2-C,3-LFE,4-Ls,5-Rs"
    channelno_userip = int(raw_input())
	
    print "Amplitude scaling factor for the channel"
    amp_scaling_factor = int(raw_input())
	
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
    NumberofChannels = int(NumChannels[0])
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
    
    if channelno_userip > NumberofChannels-1:
        print "Invalid channel number - Input has %d channels"%NumberofChannels
        print "Provide values 0 to %d"%(NumberofChannels-1)
        sys.exit(2)
        
    
    iterator_value = int(DataSize)/2;
    print iterator_value
    
    for data in range(0,iterator_value):        
        if (data % NumberofChannels) == channelno_userip:
            scaling_factor = amp_scaling_factor
        else:
            scaling_factor = 1
            
        if data < 12:
            scaling_factor = 1
            
        stringleft = fin.read(2)
        S1=struct.unpack("h",stringleft)
        packed_value_new = int(S1[0]) * scaling_factor
        if packed_value_new > 32767 or packed_value_new < -32768:
            packed_value_new = int(S1[0])
        packed_value_new1 = struct.pack("h",packed_value_new)
        fout.write(packed_value_new1)                   
    fin.close()
    fout.close()

def swapChannelAmplitude(input_file,output_file):

    headerbytes = 0
    NumberofChannels = 0
    channel_sample = [None]*6
    
    destination_folder = "C:\\AudioTest-API\\Python_SampleModified_Files\\"
    
    output_file = destination_folder + os.path.splitext(os.path.basename(output_file))[0] + ".wav"
    
    # open(fname,mode) is the Python way of reading files
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"wb")
	
    print "Enter the channel no for sample swap - 0-L,1-R,2-C,3-LFE,4-Ls,5-Rs"
    print "Enter Channel A:"
    channel_A = int(raw_input())
    print "Enter Channel B:"
    channel_B = int(raw_input())
	
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
    NumberofChannels = int(NumChannels[0])
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
    
    if channel_A > NumberofChannels-1 or channel_B > NumberofChannels-1:
        print "Invalid channel number - Input has %d channels"%NumberofChannels
        print "Provide values 0 to %d"%(NumberofChannels-1)
        sys.exit(2)
        
    
    iterator_value = int(DataSize)/(2 * NumberofChannels);
    print iterator_value
    
    for data in range(0,iterator_value):
        for ch in range(0,NumberofChannels):
            stringleft = fin.read(2)
            #S1=struct.unpack("h",stringleft)
            #packed_value_new = int(S1[0])
            #packed_value_new1 = struct.pack("h",packed_value_new)
            channel_sample[ch] = stringleft
        
        if data >= (4 * NumberofChannels):
            temp = channel_sample[channel_B] 
            channel_sample[channel_B] = channel_sample[channel_A]
            channel_sample[channel_A] = temp
        
        for ch1 in range(0,NumberofChannels):
            fout.write(channel_sample[ch1])
        
    fin.close()
    fout.close()
    
def sampleCorruption(input_file,output_file):
    
    headerbytes = 0
    NumberofChannels = 0
    
    destination_folder = "C:\\AudioTest-API\\Python_SampleModified_Files\\"
    
    output_file = destination_folder + os.path.splitext(os.path.basename(output_file))[0] + ".wav"
    
    # open(fname,mode) is the Python way of reading files
    fin = open(input_file,"rb") # Read wav file, "r flag" - read, "b flag" - binary 
    fout = open(output_file,"wb")
	
    print "Enter the channel no for sample corruption - 0-L,1-R,2-C,3-LFE,4-Ls,5-Rs"
    channel_no = int(raw_input())    
    
    print "Enter the sample frequencey for corruption - ~100 samples for every sampling frequency will be corrupted with a random value"
    corruption_freq = float(raw_input())
	
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
    NumberofChannels = int(NumChannels[0])
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
    ByteRate = int(ByteRate[0])
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
    
    if channel_no > NumberofChannels-1:
        print "Invalid channel number - Input has %d channels"%NumberofChannels
        print "Provide values 0 to %d"%(NumberofChannels-1)
        sys.exit(2)
            
    count = 0
    time_interval = 0
    start_corruption = False
    iterator_value = int(DataSize)/2 ;
    print iterator_value

    for data in range(0,iterator_value):
        if (data % (corruption_freq * ByteRate)/2) == 0:
            start_corruption = True
            count = 0            
                    
        if start_corruption == True and (data % NumberofChannels) == channel_no and count < 2:
            scaling_factor = 2
            count = count + 1
            if count >= 2:
                start_corruption = False
                count = 0
                scaling_factor = 1
        else:
            scaling_factor = 1
            
        if data < (4 * NumberofChannels):
            scaling_factor = 1
            
        stringleft = fin.read(2)
        S1=struct.unpack("h",stringleft)
        packed_value_new = int(S1[0]) * scaling_factor
        if packed_value_new > 32767 or packed_value_new < -32768:
            packed_value_new = int(S1[0])
        packed_value_new1 = struct.pack("h",packed_value_new)
        fout.write(packed_value_new1)
                        
    fin.close()
    fout.close()
    

if __name__ == "__main__":
    
    try:
        inputfile = ''
        outputfile = ''
        opValidationOption = 255
        try:
            opts, args = getopt.getopt(sys.argv[1:],"hi:o:x:",["ifile=","ofile=","xoption="])
        except getopt.GetoptError:
            print 'Usage error.'
            print 'Usage: ' + sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-AmplitudeChange,2-ChannelSwap,3-ChannelSampleCorruption> '
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-AmplitudeChange,2-ChannelSwap,3-ChannelSampleCorruption> '
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = os.path.abspath(arg)
            elif opt in ("-o", "--ofile"):
                outputfile = os.path.abspath(arg)
            elif opt in ("-x", "--xoption"):
                ipFileModifierOption = arg
                                
        if inputfile == '' or outputfile == '' or opValidationOption == '':
            print 'Usage error.'
            print 'Usage: ' + sys.argv[0] + ' -i <inputfile> -o <outputfile> -x <1-AmplitudeChange,2-ChannelSwap,3-ChannelSampleCorruption> '
            sys.exit(2)
            
        ip_filename, ip_file_extension = os.path.splitext(inputfile)
    
        if ip_file_extension != '.wav':
            print "wrong file format - Input file format must be .wav"    
    
        if ipFileModifierOption == '1':
            changeChannelAmplitude(inputfile,outputfile)
        elif ipFileModifierOption == '2':
            swapChannelAmplitude(inputfile,outputfile)
        elif ipFileModifierOption == '3':
            sampleCorruption(inputfile,outputfile)
        else:
            print "Invalid option - Use Help for valid options"

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
