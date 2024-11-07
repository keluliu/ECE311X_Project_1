import numpy as np
import adi
import matplotlib.pyplot as plt
import time

# Define parameters
sample_rate = 10e6  # Sampling rate in Hz
center_freq = 2.4e9  # Center frequency set to 2.4 GHz
bandwidth = center_freq / 4  # Bandwidth calculated as a quarter of the center frequency
fft_size = 1024  # Size of each FFT
buff_size = 2**20  # Buffer size for receiving samples
num_ffts = buff_size // fft_size  # Number of FFTs to compute

# Create an instance of the Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")

# Configure the SDR
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = buff_size

# Receive samples
samples = sdr.rx()

# Prepare a 2D array to hold FFT results
waterfall_2darray = np.zeros((num_ffts, fft_size))

# Function to compute FFT and shift the zero frequency component to the center
def compute_fft(samples):
    return np.fft.fftshift(np.fft.fft(samples))

# Calculate FFTs for the received samples
for i in range(num_ffts):
    x = samples[i * fft_size:(i + 1) * fft_size]
    fft_result = compute_fft(x)
    waterfall_2darray[i, :] = np.log10(abs(fft_result))

# Duration of the buffer in milliseconds
block_duration_ms = (buff_size / sample_rate) * 1000

# Plotting the waterfall spectrogram
plt.imshow(waterfall_2darray, aspect='auto', extent=[-sample_rate/2, sample_rate/2, 0, block_duration_ms], cmap='viridis')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Time (ms)')
plt.title('Spectrogram of Wireless Transmission')
plt.colorbar(label='Magnitude')
plt.show()

# Define time axis for the time-domain signal
time_axis = np.arange(len(samples)) / sample_rate * 1000  # in ms

# Plot time-domain signal with both Real and Imaginary parts in the same subplot
plt.figure(figsize=(12, 6))
plt.plot(time_axis, samples.real, label="Real", color="blue", alpha=0.7)  # Plot Real part
plt.plot(time_axis, samples.imag, label="Imaginary", color="orange", alpha=0.7)  # Plot Imaginary part

plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal")
plt.legend()
plt.grid()
plt.xlim([0, (len(samples) / sample_rate) * 1000])  # Set x-axis limit based on total time
plt.ylim([-2500, 2500])  # Adjust y-axis limits for better visibility
plt.tight_layout()
plt.show()
