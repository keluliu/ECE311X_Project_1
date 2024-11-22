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

# Calculate frequency offset (coarse estimation)
# Here, we determine the peak in the frequency domain to estimate the offset
avg_fft = np.mean(waterfall_2darray, axis=0)
peak_index = np.argmax(avg_fft)
freq_axis = np.linspace(-sample_rate / 2, sample_rate / 2, fft_size)
freq_offset = freq_axis[peak_index]

# Adjust SDR center frequency to correct the offset
corrected_center_freq = center_freq + freq_offset
sdr.rx_lo = int(corrected_center_freq)

# Collect data again after frequency correction
corrected_samples = []
for iteration in range(num_iterations):
    print(f"Collecting corrected data chunk {iteration + 1} of {num_iterations}...")
    samples = sdr.rx()
    corrected_samples.append(samples)

# Concatenate all corrected samples to create a new 25-second dataset
corrected_samples = np.concatenate(corrected_samples)

# Plot magnitude and phase before and after correction
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Define time axis for time-domain plot
time_axis = np.arange(len(all_samples)) / sample_rate * 1000
downsample_factor = 100  # Plot every 100th sample to reduce memory usage
downsampled_time_axis = time_axis[::downsample_factor]

# Magnitude and Phase before correction
downsampled_magnitude_before = np.sqrt(all_samples.real[::downsample_factor]**2 + all_samples.imag[::downsample_factor]**2)
downsampled_phase_before = np.angle(all_samples)[::downsample_factor]

axs[0, 0].plot(downsampled_time_axis, downsampled_magnitude_before, color="blue")
axs[0, 0].set_title("Magnitude Before Correction")
axs[0, 0].set_xlabel("Time (ms)")
axs[0, 0].set_ylabel("Magnitude")

axs[1, 0].plot(downsampled_time_axis, downsampled_phase_before, color="orange")
axs[1, 0].set_title("Phase Before Correction")
axs[1, 0].set_xlabel("Time (ms)")
axs[1, 0].set_ylabel("Phase (radians)")

# Magnitude and Phase after correction
downsampled_magnitude_after = np.sqrt(corrected_samples.real[::downsample_factor]**2 + corrected_samples.imag[::downsample_factor]**2)
downsampled_phase_after = np.angle(corrected_samples)[::downsample_factor]

axs[0, 1].plot(downsampled_time_axis, downsampled_magnitude_after, color="green")
axs[0, 1].set_title("Magnitude After Correction")
axs[0, 1].set_xlabel("Time (ms)")
axs[0, 1].set_ylabel("Magnitude")

axs[1, 1].plot(downsampled_time_axis, downsampled_phase_after, color="red")
axs[1, 1].set_title("Phase After Correction")
axs[1, 1].set_xlabel("Time (ms)")
axs[1, 1].set_ylabel("Phase (radians)")

plt.tight_layout()
plt.show()

# Plot Constellation Diagrams before and after correction
plt.figure(figsize=(12, 6))

# Constellation Before Correction
plt.subplot(1, 2, 1)
plt.scatter(all_samples.real[::downsample_factor], all_samples.imag[::downsample_factor], s=1, alpha=0.6)
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram Before Correction")
plt.grid(True)
plt.axis('equal')

# Constellation After Correction
plt.subplot(1, 2, 2)
plt.scatter(corrected_samples.real[::downsample_factor], corrected_samples.imag[::downsample_factor], s=1, alpha=0.6)
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram After Correction")
plt.grid(True)
plt.axis('equal')

plt.tight_layout()
plt.show()
