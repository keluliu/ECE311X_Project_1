import numpy as np
import adi
import matplotlib.pyplot as plt
import time

# Define parameters
sample_rate = 10e6  # Sampling rate in Hz
center_freq = 433.9e6  # Center frequency set to 433.9 MHz
bandwidth = center_freq / 4  # Bandwidth calculated as a quarter of the center frequency
fft_size = 1024  # Size of each FFT
buff_size = 10_000_000  # Smaller buffer size to avoid "File too large" error
num_ffts = buff_size // fft_size  # Number of FFTs to compute

# Create an instance of the Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")

# Configure the SDR
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = buff_size

# Calculate total samples for 20 seconds
total_samples_needed = int(sample_rate * 20)  # Total samples for 20 seconds
data_buffer = []

# Collect data in segments
while len(data_buffer) < total_samples_needed:
    samples = sdr.rx()  # Receive data
    data_buffer.extend(samples)  # Append received data to buffer

# Convert collected data to a NumPy array
data_array = np.array(data_buffer)

# Prepare a 2D array to hold FFT results
num_ffts = len(data_array) // fft_size  # Update number of FFTs based on collected data length
waterfall_2darray = np.zeros((num_ffts, fft_size))

# Function to compute FFT and shift the zero frequency component to the center
def compute_fft(samples):
    return np.fft.fftshift(np.fft.fft(samples))

# Calculate FFTs for the received samples
for i in range(num_ffts):
    x = data_array[i * fft_size:(i + 1) * fft_size]
    fft_result = compute_fft(x)
    waterfall_2darray[i, :] = np.log10(abs(fft_result))

# Duration of the buffer in milliseconds
block_duration_ms = (len(data_array) / sample_rate) * 1000

# Plotting the waterfall spectrogram
plt.imshow(waterfall_2darray, aspect='auto', extent=[-sample_rate/2, sample_rate/2, 0, block_duration_ms], cmap='viridis')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Time (ms)')
plt.title('Spectrogram of Wireless Transmission')
plt.colorbar(label='Magnitude')
plt.show()

# Define time axis for the time-domain signal
time_axis = np.arange(len(data_array)) / sample_rate * 1000  # in ms

# Plot time-domain signal with both Real and Imaginary parts in the same subplot
plt.figure(figsize=(12, 6))
plt.plot(time_axis, data_array.real, label="Real", color="blue")  # Plot Real part
plt.plot(time_axis, data_array.imag, label="Imaginary", color="orange")  # Plot Imaginary part

plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal")
plt.legend()
plt.grid()
plt.xlim([0, 20000])  # Set x-axis limit based on total time for 20 seconds
plt.ylim([-2500, 2500])  # Adjust y-axis limits for better visibility
plt.tight_layout()
plt.show()
