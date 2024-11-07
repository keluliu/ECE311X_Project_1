import numpy as np
import adi
import matplotlib.pyplot as plt
import time

sample_rate = 10e6

center_freq = 2.4e9
bandwidth = center_freq/4
fft_size = 1024
buff_size = 2**20
num_ffts = buff_size//fft_size

sdr = adi.Pluto("ip:192.168.2.1")

sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = buff_size

samples = sdr.rx()

waterfall_2darray = np.zeros((num_ffts, fft_size))

def compute_fft(samples):
    return np.fft.fftshift((np.fft.fft(samples)))

for i in range(num_ffts):
    x = samples[i*fft_size:(i+1)*fft_size]
    fft_result = compute_fft(x)
    waterfall_2darray[i, :] = np.log10(abs(fft_result))

block_duration_ms = (buff_size / sample_rate) * 1000

plt.imshow(waterfall_2darray, aspect='auto', extent = [-sample_rate/2, sample_rate/2, 0, block_duration_ms], cmap='viridis')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Time (ms)')
plt.title('Spectrogram')
plt.colorbar(label='Magnitude')
plt.show()

# Define time axis
time_axis = np.arange(len(samples)) / sample_rate * 1000

# Plot time-domain signal with separate subplots
plt.figure(figsize=(12, 8))

# Plot Real Part
plt.subplot(2, 1, 1)
plt.plot(time_axis, samples.real, label="Real", color="blue")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal (Real Part)")
plt.legend()

# Plot Imaginary Part
plt.subplot(2, 1, 2)
plt.plot(time_axis, samples.imag, label="Imaginary", color="orange")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal (Imaginary Part)")
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
