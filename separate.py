# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:54:43 2018

@author: yui_sudo


"""

from sound import WavfileOperate
import os

class1_list = os.listdir(os.getcwd())
class1_list.sort()

for class1 in class1_list:
    print(class1)
    class1_dir =  os.getcwd() + "/" + class1 + "/"
    if os.path.isdir(class1_dir) == True:
        class2_list = os.listdir(class1_dir)
        class2_list.sort()
        
        for class2 in class2_list:
            class2_dir =  class1_dir + class2 + "/"
            filelist = os.listdir(class2_dir)
            filelist.sort()
            print(class2)
            for filename in filelist:
                if filename[-3:] == "wav" or filename[-3:] == "WAV":
                    wave = WavfileOperate(class2_dir + "/" + filename).wavedata
                    if len(wave.norm_sound) > 131072:
                        for i in range(len(wave.norm_sound)//131072):
                            
                            wave.cut_wav(i*8.192, (i+1)*8.192).write_wav_sf(dir=class2_dir, filename=filename[:-4]+"_"+str(i)+".wav", bit=16)
                        os.remove(class2_dir + "/" + filename)
                            