import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from pluto_lib import PlutoSDR
from scipy import signal
from time import sleep

#allows plots to display in the notebook instead of another window
%matplotlib inline




RXLO = int(914e6) # center frequency to tune to
# RXLO = int(2410e6)
# RXLO = int(462e6) # around the frequency of blue radio
RXBW = int(40e6) # bandwidth
RXFS = int(40e6) # sample rate

sdr = PlutoSDR()

sdr.rx_rf_port_select_chan0 = "A_BALANCED"
sdr.rx_lo = RXLO
sdr.sample_rate = RXFS
sdr.gain_control_mode_chan0 = "slow_attack"
sdr.rx_buffer_size = int(40e3)

fft_size = 40000
num_rows = 500

# raw_samples = np.zeros((num_rows, 30000), dtype=np.complex64)
rx_samples = np.zeros((num_rows,fft_size), dtype=np.complex64)

#generate 5ms intervals for 1 second
t = np.arange(int(sdr.rx_buffer_size*num_rows))/RXFS





for k in range(500):
    rx_samples[k,:40000] = sdr.rx()
# print(raw_samples)




rx_samples[:,:30000] = raw_samples[:,:30000]
for i in range(num_rows):
    rx_samples[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(rx_samples[i], fft_size)))**2)

rx_samples = rx_samples.astype('float64')

#generates the spectogram
plt.imshow(rx_samples, aspect='auto', extent=[-RXFS/2/1e6, RXFS/2/1e6, 0, 200])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [5 ms]")

stepper = 0





f = np.linspace(RXFS/-2, RXFS/2, len(rx_samples[0]))

sleep(0.5)
plt.figure()
plt.plot(f, rx_samples[stepper])
stepper += 1
print(stepper)





#configure tx
sdr.tx_rf_bandwidth = RXBW
sdr.tx_lo = RXLO
sdr.tx_hardwaregain_chan0 = -50
print(raw_samples[42]*2**6)

for i in range(200):
    sdr.tx(raw_samples[i]*2**1)





spectogram = np.zeros((500,1024), dtype=np.float64)
for i in range(num_rows):
    _, psd = signal.welch(rx_samples[i,:40000], RXFS, 'flattop', 1024, return_onesided=False, scaling='spectrum', average='median')
    psd_dB = 10*np.log10((np.abs(psd)/psd.shape[0])**2)
    spectogram[i,:] = np.fft.fftshift(psd_dB)

#generates the spectogram
left_bound = (RXLO - RXFS/2)/1e6
right_bound = (RXLO + RXFS/2)/1e6
plt.imshow(spectogram, aspect='auto', extent=[left_bound, right_bound, 0, num_rows])
plt.xlabel("Frequency [MHz]")
plt.ylabel("Time [5 ms]")







