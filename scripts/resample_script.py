# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:54:43 2018

@author: yui_sudo


"""

from sound import WavfileOperate
import os
import shutil


filelist = os.listdir(os.getcwd())
for filename in filelist:
    if filename[-3:] == "wav" or filename[-3:] == "WAV":
        wave = WavfileOperate(os.getcwd() + "/" + filename)
        if wave.nchan == 1:
            wave = wave.wavedata            
        elif wave.nchan == 2:
            wave = wave.wavedata[0]
        
        if wave.fs == 16000:
            print("This file is already 16kHz")
            #wave.write_wav_sf(dir=current_dir+"/", filename="16kHz_" + filename, bit=16)
            #break
        else:
            fs = str(wave.fs//1000) + "kHz"
            up = 16000
            down = wave.fs
            wave = wave.resample_poly(up_n=up, down_n=down)
            wave.write_wav_sf(dir=os.getcwd()+"/", filename="16kHz_" + filename, bit=16)
            os.remove(os.getcwd() + "/" + filename)
            print(os.getcwd())
            print("Successfully resample from", fs, "to 16kHz and save it")
            
shutil.rmtree(os.getcwd() + "/__pycache__")