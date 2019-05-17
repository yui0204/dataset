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

from sound import WavfileOperate, Wavedata, Multiwave
import random

import shutil
import scipy


def sampling_reverb(signal_array, impulse_response, tf):
    
    sigL = len(signal_array)
    new_irL = 512
    frameL = new_irL // 2
    frame_num = 257
    new_sigL = frameL * frame_num
    new_sig = np.zeros(new_sigL, dtype = np.float64)
    new_sig = signal_array
    
    ret = np.zeros(new_sigL, dtype = np.float64)

    ir_fft = tf * 0.6
    for ii in range(frame_num - 1):
        s_ind = frameL * ii
        e_ind = frameL * (ii + 2)
        
        sig_fft = scipy.fftpack.fft(new_sig[s_ind : e_ind])        
        ret[s_ind:s_ind + frameL] = scipy.ifft(sig_fft * ir_fft)[frameL:].real

    return ret[:sigL]


def multi_conv(sig_wavedata, ir_multiwave, tf):    
    wavedata_list = []
    for n in range(ir_multiwave.nchan):
        con = sampling_reverb(sig_wavedata.norm_sound, ir_multiwave.norm_sound[n], tf[n])
        conv = Wavedata(16000, con, sig_wavedata.name, sig_wavedata.nbyte)
        wavedata_list.append(conv)

    return wavedata_list[0], Multiwave(wavedata_list)
    
       
overlap = 0.75

for image_size in [256]:
    total_length = image_size * 256 + 256
    n = 3
    for mode in ["train", "val"]:
        dry_dir = os.getcwd() + "/elements/"+mode+"/"
        if mode == "train":
<<<<<<< HEAD
            totalnum = 3000
        else:
            totalnum = 500
=======
            totalnum = 1000
        else:
            totalnum = 100
>>>>>>> 889a559a26ac3323c51ec6b8731c59972cbb2b24
        for datanum in range(0, totalnum):
            print("\n\n\nNo.", datanum)   
            name = ""
            namelist = []
            namelist2 = []
            wavelist = []
            multiwavelist = []
            text = ""
            same = False
            
            idx = 0
            long_n = 0
            short_n = 0
            #for i in range(n):
            for i in range(n):
                # a1, a2, b1, b2 ...
                dir1_list = os.listdir(dry_dir)
                #dir1 = dir1_list[random.randrange(len(dir1_list))]     
                
                dir1 = "HUMAN/"
                
                cur_dir = dry_dir + dir1        
                if os.path.isdir(cur_dir) == True:        
                    dir2_list = os.listdir(cur_dir)
                    #dir2 = dir2_list[random.randrange(len(dir2_list))]            
                    if i == 0:                        
<<<<<<< HEAD
                        dir2 = dir2_list[2]
                    elif i == 1 or i == 2:               
                        dir2 = dir2_list[i * 2 + 1]
=======
                        dir2 = dir2_list[2] # COUGH
                    elif i == 1 or i == 2:               
                        dir2 = dir2_list[i * 2 + 1] # FART, THROAT
>>>>>>> 889a559a26ac3323c51ec6b8731c59972cbb2b24

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
        
                        if wave.norm_sound.max() > 1.0:
                                print("clipping!!!!!!!!!!!!!!!!!!!")
                                print(wave.norm_sound.max())
                        ### wave conv
                        ir_dir = "./impulse_response/"
<<<<<<< HEAD
                        #deg = random.randrange(8) * 45
                        deg = i * 90
=======
                        deg = random.randrange(8) * 45
                        #deg = i * 90
>>>>>>> 889a559a26ac3323c51ec6b8731c59972cbb2b24
                        tf = np.load(ir_dir+"tf_" + str(deg) + "deg.npy")
                        ir_multi = WavfileOperate(ir_dir+"impulse_"+str(deg)+"deg.wav", logger=1).multiwave
                        #print(ir_multi.name)
                        wave, multiwave = multi_conv(wave, ir_multi, tf)
                        
                        for nchan in range(8):
                            if multiwave.norm_sound[nchan].max() > 1.0:
                                multiwave.plot()
                                print("clipping!!!!!!!!!!!!!!!!!!!")
                                print(multiwave.norm_sound[nchan].max())
                            
                        if not len(multiwave.norm_sound[0]) == total_length:
                            print("Size error!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        
                        text = text + dir2 + "_" + str(deg) + "deg\n"
                        
                        
                            
                        if len(wavelist) == 0:
                            wavelist.append(wave)
                            name = name + "_" + dir2
                            namelist2.append(dir2)
                            syn_wave = wave
                            multi_syn_wave = multiwave
                            
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
                            multi_syn_wave = multi_syn_wave.synthesis(multiwave, synthesis_name = name)
       
                 
                        if idx >= total_length:
                            idx = 0
                            #break                   
                else:
                    continue
                
                
            for noise_db in [-20]:
<<<<<<< HEAD
                noise_segdata_dir = os.getcwd()+"/datasets/multi_segdata3_"+str(image_size)+"_"+ str(noise_db)+"dB/"+mode+"/"
                segdata_dir = os.getcwd()+"/datasets/multi_segdata3_"+str(image_size)+"_no_sound/"+mode+"/"
=======
                noise_segdata_dir = os.getcwd()+"/datasets/multi_segdata3_"+str(image_size)+"_"+ str(noise_db)+"dB_random/"+mode+"/"
                segdata_dir = os.getcwd()+"/datasets/multi_segdata3_"+str(image_size)+"_no_sound_random/"+mode+"/"
>>>>>>> 889a559a26ac3323c51ec6b8731c59972cbb2b24
                #noise_segdata_dir = os.getcwd()+"/datasets/"+dirname+"_"+str(image_size)+"_"+ str(noise_db)+"dB/"+mode+"/"
                #segdata_dir = os.getcwd()+"/datasets/"+dirname+"_"+str(image_size)+"/"+mode+"/"

                
                if datanum % 2 == 0:
                    bgm = WavfileOperate(os.getcwd()+'/BGMs/restaurant.wav').wavedata.vol(noise_db)  
                else:    
                    bgm = WavfileOperate(os.getcwd()+'/BGMs/hall.wav').wavedata.vol(noise_db)
                nframe = len(bgm.norm_sound)
                start_idx = random.randrange(nframe - 9 * bgm.fs)
                cut_sound = bgm.norm_sound[start_idx:start_idx + total_length] 
                bgm = Wavedata(bgm.fs, cut_sound, bgm.name, bgm.nbyte)
                noise_syn_wave = syn_wave.synthesis(bgm, synthesis_name = name)
                    
                no_sound = WavfileOperate(os.getcwd()+'/BGMs/no_sound.wav').wavedata.vol(0)
                syn_wave = syn_wave.synthesis(no_sound, synthesis_name=name)

                bgm_list = []
                no_sound_list = []
                for mic_chan in range(8):
                    bgm_list.append(bgm)
                    no_sound_list.append(no_sound)
                multi_bgm = Multiwave(bgm_list)
                multi_no_sound = Multiwave(no_sound_list)
                multi_syn_wave = multi_syn_wave.synthesis(multi_no_sound, synthesis_name = name)
                multi_noise_syn_wave = multi_syn_wave.synthesis(multi_bgm, synthesis_name = name)
                
                
                #noise_syn_wave.plot()
                #bgm.stft_plot()
                """
                if noise_db == -20:
                    syn_wave.stft_plot()
                noise_syn_wave.stft_plot()
                #multi_syn_wave.stft_plot()
                """
                
                noise_save_dir = noise_segdata_dir + str(datanum) + "/"  
                if not os.path.exists(noise_save_dir):
                    os.makedirs(noise_save_dir)
                save_dir = segdata_dir + str(datanum) + "/"          
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                for i in range(len(wavelist)):
                    #if noise_db == -20:
                    #    wavelist[i].stft_plot()
                    wavelist[i].write_wav_sf(dir=noise_save_dir, filename=namelist2[i] + ".wav", bit=16)
                    if noise_db == -20:
                        wavelist[i].write_wav_sf(dir=save_dir, filename=namelist2[i] + ".wav", bit=16)
                        with open(save_dir+'sound_direction.txt', 'w') as f:
                            f.write(text)
                
                bgm.write_wav_sf(dir=noise_save_dir, filename="BGM.wav", bit=16)
                noise_syn_wave.write_wav_sf(dir=noise_save_dir, filename="0_" + name + ".wav", bit=16)

                multi_noise_syn_wave.write_wav_sf(dir=noise_save_dir, filename="0_multi_" + name + ".wav", bit=16)
                if noise_db == -20:
                    syn_wave.write_wav_sf(dir=save_dir, filename="0_" + name + ".wav", bit=16)
                    multi_syn_wave.write_wav_sf(dir=save_dir, filename="0_multi_" + name + ".wav", bit=16)                
                if not os.getcwd() == '/home/yui-sudo/document/segmentation/sound_segtest':
                    shutil.copy("make_toy_dataset4_multi.py", segdata_dir)
                    shutil.copy("make_toy_dataset4_multi.py", noise_segdata_dir)
                    
                with open(noise_save_dir+'sound_direction.txt', 'w') as f:
                    f.write(text)
<<<<<<< HEAD
                
=======
                
>>>>>>> 889a559a26ac3323c51ec6b8731c59972cbb2b24
