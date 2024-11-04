# import iio
# import adi
# import numpy as np
# import sys
# import matplotlib.pyplot as plt
# from scipy import signal

# # ----------------------------------------------------------
# # Define the handmade spectrogram function
# def myspectrogram(data,N,M,Fs):
    
#     # Calculate number of windows to be processed
#     num_windows = int((len(data) - (M/2)) // (N - (M/2)))
    
#     # Generate Hamming window
#     hamming_window = np.hamming(N)

#     # Define time instances for FFT slices
#     t_spectro = np.arange(0, (num_windows)*(N*(1/Fs)), N*(1/Fs))

#     # Define FFT bin frequencies (normalized by 2\pi)
#     f_spectro = np.arange(0, 1, 1/N)

#     # Divide up data into blocks of size N, with M/2 overlap with previous
#     # block and M/2 overlap with next block, and multiple with hamming window
#     spectrogram_results = np.zeros((num_windows,N))
#     for i in range(num_windows):
#         start_ind = i*(int(N - (M/2)))
#         seg = data[start_ind:(start_ind + N)]
#         windowed_seg = seg*hamming_window
#         abs_fft_result = np.abs(np.fft.fft(windowed_seg))
#         spectrogram_results[i] = abs_fft_result

#     return t_spectro, f_spectro, spectrogram_results

# sdr = adi.Pluto("ip:192.168.2.1")
# rx_rf_bandwidth = 433000000
# data = sdr.rx()
# np.set_printoptions(threshold=sys.maxsize)
# print(data)

import iio
import adi
import numpy as np
import sys

sdr = adi.Pluto("ip:192.168.2.1")
rx_rf_bandwidth = 433000000
data = sdr.rx()
np.set_printoptions(threshold=sys.maxsize)
print(data)