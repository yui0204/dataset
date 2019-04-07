#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 23:29:14 2018

@author: yui-sudo
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sound import WavfileOperate, Wavedata
import random

import shutil
       
#dirname = "SMALL_STUFF"
overlap = 0.75


for image_size in [256]:
    total_length = image_size * 256 + 256
    n = 4
    for mode in ["train", "val"]:
        if mode == "train":
            dry_dir = os.getcwd() + "/elements/"
            totalnum = 100
        else:
            dry_dir = os.getcwd() + "/elements_val/"
            totalnum = 100
        for datanum in range(0,totalnum):
            print("\n\n\nNo.", datanum)   
            name = ""
            namelist = []
            namelist2 = []
            wavelist = []
            same = False
            
            idx = 0
            long_n = 0
            short_n = 0
            for i in range(n):
                # a1, a2, b1, b2 ...
                dir1_list = os.listdir(dry_dir)
                dir1 = dir1_list[random.randrange(len(dir1_list))]     
                
                #dir1 = dirname
                
                cur_dir = dry_dir + dir1        
                if os.path.isdir(cur_dir) == True:        
                    dir2_list = os.listdir(cur_dir)
                    dir2 = dir2_list[random.randrange(len(dir2_list))]            
                    cur_dir = cur_dir + "/" + dir2 + "/"           
                    namelist.append(dir1+"_"+dir2)                
                    data_list = os.listdir(cur_dir)
        
                    filename = cur_dir + data_list[random.randrange(len(data_list))]
                    
                    if filename[-3:] == "wav" or filename[-3:] == "wav":
                        wave = WavfileOperate(filename).wavedata
                        
                        if len(wave.norm_sound) > total_length // 1:
                            if long_n == 1:
                                wave = wave.cut_wav(0, 2, window=True)
                                
                                short_n += 1
                                length = len(wave.norm_sound)
                                if idx == 0:
                                    idx = random.randrange(5000)
                                else:
                                    idx = (idx - random.randrange(overlap * wave.fs))
    
                                if idx < 0:
                                    idx = 0
                                elif (idx + length) > total_length:
                                    wave = wave.cut_wav(0, (total_length-idx)/wave.fs, window=False)
                                    length = len(wave.norm_sound)
                                print(round(idx/wave.fs,2), "-", round((idx+length)/wave.fs,2))
                                
                                wave = wave.zero_padding(total=total_length, start_idx=idx)
                                idx += length   
                                
                                print("long_over!!!!")
                            
                            else:
                                wave = wave.cut_wav(0, 4.112, window=False)
                                long_n += 1

                        else:
                            short_n += 1

                            length = len(wave.norm_sound)
                            if idx == 0:
                                idx = random.randrange(5000)
                            else:
                                idx = (idx - random.randrange(overlap * wave.fs))

                            if idx < 0:
                                idx = 0
                            elif (idx + length) > total_length:
                                wave = wave.cut_wav(0, (total_length-idx)/wave.fs, window=False)
                                length = len(wave.norm_sound)
                            print(round(idx/wave.fs,2), "-", round((idx+length)/wave.fs,2))
                            
                            wave = wave.zero_padding(total=total_length, start_idx=idx)
                            idx += length   
                                
                            if not len(wave.norm_sound) == total_length:
                                print("Size error!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
                            
                        if len(wavelist) == 0:
                            wavelist.append(wave)
                            name = name + "_" + dir2
                            namelist2.append(dir2)
                            syn_wave = wave
                        elif len(wavelist) > 0:
                            for j in range(len(namelist2)):
                                if dir2 == namelist2[j]:
                                    wavelist[j] = wavelist[j].synthesis(wave, synthesis_name=dir2)
                                    same = True
                                    break
                            if same == False:
                                wavelist.append(wave)
                                name = name + " " + dir2
                                namelist2.append(dir2)
                            same = False
                            syn_wave = syn_wave.synthesis(wave, synthesis_name = name)
                    
                        if idx >= total_length:
                            idx = 0
                            #break                   
                else:
                    continue
            for noise_db in [-30, -20, -10, 0]:
                noise_segdata_dir = os.getcwd()+"/segdata76_"+str(image_size)+"_"+ str(noise_db)+"dB/"+mode+"/"
                segdata_dir = os.getcwd()+"/segdata75_"+str(image_size)+"_no_sound/"+mode+"/"
        #        noise_segdata_dir = os.getcwd()+"/"+dirname+"10_"+str(image_size)+"_"+ str(noise_db)+"dB/"+mode+"/"
        #        segdata_dir = os.getcwd()+"/"+dirname+"9_"+str(image_size)+"/"+mode+"/"

                
                if datanum % 2 == 0:
                    bgm = WavfileOperate(os.getcwd()+'/restaurant.wav').wavedata.vol(noise_db)  
                else:    
                    bgm = WavfileOperate(os.getcwd()+'/hall.wav').wavedata.vol(noise_db)
                nframe = len(bgm.norm_sound)
                start_idx = random.randrange(nframe - 9 * bgm.fs)
                cut_sound = bgm.norm_sound[start_idx:start_idx + total_length] 
                bgm = Wavedata(bgm.fs, cut_sound, bgm.name, bgm.nbyte)   
                noise_syn_wave = syn_wave.synthesis(bgm, synthesis_name = name)
    
                no_sound = WavfileOperate(os.getcwd()+'/no_sound.wav').wavedata.vol(0)
                syn_wave = syn_wave.synthesis(no_sound, synthesis_name = name)
                
                
                #noise_syn_wave.plot()
                #bgm.stft_plot()
                if noise_db == -30:
                    syn_wave.stft_plot()
                noise_syn_wave.stft_plot()  
                
                # Mixデータのフォルダ作成
                noise_save_dir = noise_segdata_dir + str(datanum) + "/"  
                if not os.path.exists(noise_save_dir):
                    os.makedirs(noise_save_dir)
                save_dir = segdata_dir + str(datanum) + "/"          
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                for i in range(len(wavelist)):
                    if noise_db == -30:
                        wavelist[i].stft_plot()
                    wavelist[i].write_wav_sf(dir=noise_save_dir, filename=namelist2[i] + ".wav", bit=16)
                    if noise_db == -30:
                        wavelist[i].write_wav_sf(dir=save_dir, filename=namelist2[i] + ".wav", bit=16)
                bgm.write_wav_sf(dir=noise_save_dir, filename="BGM.wav", bit=16)
                noise_syn_wave.write_wav_sf(dir=noise_save_dir, filename="0_" + name + ".wav", bit=16)
                if noise_db == -30:
                    syn_wave.write_wav_sf(dir=save_dir, filename="0_" + name + ".wav", bit=16)
                
                if not os.getcwd() == '/home/yui-sudo/document/segmentation/sound_segtest':
                    shutil.copy("make_dataset4.py", segdata_dir)
                    shutil.copy("make_dataset4.py", noise_segdata_dir)
