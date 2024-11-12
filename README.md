import numpy as np
import adi
import matplotlib.pyplot as plt

# Adjusted sample rate to achieve 2500 ms block duration
sample_rate = 1_678_000  # Approximately 1.678 Msps

center_freq = 433.9e6
bandwidth = center_freq / 4
fft_size = 1024
buff_size = 2**22  # 4,194,304 samples
num_ffts = buff_size // fft_size
num_iterations = 10  # To gather 25 seconds worth of data

# Initialize SDR
sdr = adi.Pluto("ip:192.168.2.1")

# Configure SDR parameters
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = buff_size

# Placeholder to gather all samples for 25 seconds
all_samples = []

# Collect data in 10 iterations (each iteration collects 2.5 seconds of data)
for iteration in range(num_iterations):
    print(f"Collecting data chunk {iteration + 1} of {num_iterations}...")
    samples = sdr.rx()
    all_samples.append(samples)

# Concatenate all samples to create a 25-second dataset
all_samples = np.concatenate(all_samples)

# Print information
total_duration_ms = (len(all_samples) / sample_rate) * 1000
print("Total Duration (ms):", total_duration_ms)

# Calculate total number of FFTs after concatenation
total_num_ffts = len(all_samples) // fft_size

# Initialize 2D array for the waterfall plot
waterfall_2darray = np.zeros((total_num_ffts, fft_size))

# Function to compute FFT
def compute_fft(samples):
    return np.fft.fftshift(np.fft.fft(samples))

# Compute FFT for each segment of the concatenated samples
for i in range(total_num_ffts):
    x = all_samples[i * fft_size : (i + 1) * fft_size]
    fft_result = compute_fft(x)
    waterfall_2darray[i, :] = np.log10(abs(fft_result))

# Calculate block duration in milliseconds for the entire dataset
block_duration_ms = (len(all_samples) / sample_rate) * 1000

# Plot spectrogram (waterfall plot)
plt.imshow(
    waterfall_2darray,
    aspect="auto",
    extent=[-sample_rate / 2, sample_rate / 2, 0, block_duration_ms],
    cmap="viridis"
)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Time (ms)")
plt.title("Spectrogram for 25 Seconds of Data")
plt.colorbar(label="Magnitude")
plt.show()

# Define time axis for time-domain plot
time_axis = np.arange(len(all_samples)) / sample_rate * 1000

# Downsample data for plotting (reduce data points to prevent memory issues)
downsample_factor = 100  # Plot every 100th sample to reduce memory usage
downsampled_time_axis = time_axis[::downsample_factor]
downsampled_samples_real = all_samples.real[::downsample_factor]
downsampled_samples_imag = all_samples.imag[::downsample_factor]

# Calculate magnitude using arithmetic operations (instead of np.abs)
downsampled_magnitude = np.sqrt(downsampled_samples_real**2 + downsampled_samples_imag**2)

# Calculate phase
downsampled_phase = np.angle(all_samples)[::downsample_factor]

# Plot time-domain signal with magnitude and phase (using downsampled data)
plt.figure(figsize=(12, 8))

# Plot Magnitude
plt.subplot(2, 1, 1)
plt.plot(downsampled_time_axis, downsampled_magnitude, label="Magnitude", color="blue")
plt.xlabel("Time (ms)")
plt.ylabel("Magnitude")
plt.title("Time-Domain Signal (Magnitude) for 25 Seconds of Data (Downsampled, Arithmetic Calculation)")
plt.legend()

# Plot Phase
plt.subplot(2, 1, 2)
plt.plot(downsampled_time_axis, downsampled_phase, label="Phase", color="orange")
plt.xlabel("Time (ms)")
plt.ylabel("Phase (radians)")
plt.title("Time-Domain Signal (Phase) for 25 Seconds of Data (Downsampled)")
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
