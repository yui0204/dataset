# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:54:43 2018

@author: yui_sudo


"""

import csv
import numpy as np
import sys
import pylab
from scipy import fftpack
import soundfile as sf
from sound import WavfileOperate, Stft, Multiwave, Wavedata

for ang in range(8):
    dat = np.loadtxt("tf0000" + str(ang) + ".csv", delimiter=",")
    datcomp = dat[:, ::2] + 1j * dat[:, 1::2]
    datfull = np.c_[np.conj(datcomp), np.fliplr((datcomp))]
    datfull = datfull[:, 1:-1]
    
    # datfull
    # 0Hz, fs/nfft Hz, 2*fs/nfft Hz, ..., nfft Hz, nfftHz, ..., fs/nfft Hz
    
    #flt = pylab.ifft2(datfull)[:, :datfull.shape[1]/2]
    flt = fftpack.ifft(datfull)[:, :]
    flt = abs(flt.T)
    sf.write("impulse_" + str(ang * 45) + "deg.wav", flt, 16000, subtype="PCM_24")
    """
    for nch in range(flt.shape[0]):
        pylab.subplot(flt.shape[0], 1, nch+1)
        pylab.plot(flt[nch, :])
        pylab.show()
    """