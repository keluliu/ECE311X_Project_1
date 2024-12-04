import numpy as np
import adi
import matplotlib.pyplot as plt

# Constants for Module 4
sample_rate = 2_000_000  # 2 Msps (suitable sample rate for the BPSK signal)
center_freq = 2.426e9  # 2.426 GHz (transmitter frequency)
buff_size = 2**20  # 1,048,576 samples for efficient processing
num_iterations = 10  # To gather 10 blocks of data for analysis

# Initialize SDR
sdr = adi.Pluto("ip:192.168.2.1")

# Configure SDR parameters
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)  # Set bandwidth to match sample rate
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = buff_size

# Placeholder to gather all samples
all_samples = []

# Collect data from the SDR
for iteration in range(num_iterations):
    print(f"Collecting data chunk {iteration + 1} of {num_iterations}...")
    samples = sdr.rx()
    all_samples.append(samples)

# Concatenate all samples for offline processing
all_samples = np.concatenate(all_samples)

# Save raw I/Q samples to a file for offline processing
np.save("bpsk_signal_raw.npy", all_samples)

# Plotting the spectrogram of the collected data
plt.figure(figsize=(10, 6))
plt.specgram(all_samples, NFFT=1024, Fs=sample_rate, noverlap=512, cmap="viridis")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram of Collected BPSK Signal")
plt.colorbar(label="Magnitude (dB)")
plt.show()

# Parameters for the Costas Loop
loop_bandwidth = 0.01  # Loop filter bandwidth (adjust as needed for stable lock)
phase_error_integral = 0  # Integrator part of loop filter
carrier_phase = 0  # Initial carrier phase

# Placeholder arrays for tracking phase and corrected samples
phase_error_history = []
corrected_samples = []

# Iterate through the signal and apply the Costas Loop
for sample in all_samples:
    # Apply the current phase correction to the sample
    corrected_sample = sample * np.exp(-1j * carrier_phase)
    corrected_samples.append(corrected_sample)

    # Calculate phase error based on the imaginary part (for BPSK)
    phase_error = np.sign(corrected_sample.real) * corrected_sample.imag
    phase_error_history.append(phase_error)

    # Update loop filter (proportional-integral controller)
    phase_error_integral += loop_bandwidth * phase_error
    carrier_phase += phase_error_integral

# Convert lists to numpy arrays for plotting
corrected_samples = np.array(corrected_samples)
phase_error_history = np.array(phase_error_history)

# Plotting the signal constellation diagrams before and after correction
plt.figure(figsize=(12, 6))

# Constellation Before Correction
plt.subplot(1, 2, 1)
plt.scatter(all_samples.real[::100], all_samples.imag[::100], s=1, alpha=0.6)
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram Before Correction")
plt.grid(True)
plt.axis('equal')

# Constellation After Correction
plt.subplot(1, 2, 2)
plt.scatter(corrected_samples.real[::100], corrected_samples.imag[::100], s=1, alpha=0.6)
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.title("Constellation Diagram After Correction")
plt.grid(True)
plt.axis('equal')

plt.tight_layout()
plt.show()

# Plotting phase error as a function of time
plt.figure(figsize=(10, 4))
plt.plot(phase_error_history, color="purple")
plt.xlabel("Sample Index")
plt.ylabel("Phase Error")
plt.title("Phase Error vs. Time (DPLL Behavior)")
plt.grid(True)
plt.show()
