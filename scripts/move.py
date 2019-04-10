# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:54:43 2018

@author: yui_sudo


"""

#from sound import WavfileOperate
import os
import shutil



class1_list = os.listdir(os.getcwd() + "/elements")
class1_list.sort()

for class1 in class1_list:
    print(class1)
    class1_dir =  os.getcwd() + "/elements/" + class1 + "/"
    if os.path.isdir(class1_dir) == True:
        class2_list = os.listdir(class1_dir)
        class2_list.sort()
        #os.makedirs(os.getcwd()+"/elements_val/"+class1)
        for class2 in class2_list:
            class2_dir =  class1_dir + class2 + "/"
            filelist = os.listdir(class2_dir)
            filelist.sort()
            #os.makedirs(os.getcwd()+"/elements_val/"+class1+"/"+class2)
            print(class2)
            for filename in filelist[int(len(filelist)*0.8):]:
                if filename[-3:] == "wav" or filename[-3:] == "WAV":
                    shutil.move(os.getcwd()+"/elements/"+class1+"/"+class2+"/"+filename, os.getcwd()+"/elements_val/"+class1+"/"+class2)
                    print(class1, class2, filename)
