# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:54:43 2018

@author: yui_sudo


"""

#from sound import WavfileOperate
import os
import shutil


filelist = os.listdir(os.getcwd())
filelist.sort()
filelist.reverse()
for filename in filelist:
    if filename[-3:] == "wav" or filename[-3:] == "WAV":
        #wave = WavfileOperate(os.getcwd() + "/" + filename)
        
        #if wave.fs == 16000:
#        no = str(int(filename[6:8])+88)
#        newname = filename[:6] + no + filename[8:19] + no + ".wav"
    
#        no = str(int(filename[:-4])+100)
#        newname = no + ".wav"
        
        
        no = str(int(filename[12:14])+60)
        newname = filename[:12] + no + filename[14:]
        
        os.rename(filename, newname)
        #break
        #shutil.move(newname, "..\\")

            
#shutil.rmtree(os.getcwd() + "/__pycache__")