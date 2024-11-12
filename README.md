# Import necessary libraries
import numpy as np
import adi  # ADI library for Pluto SDR
import matplotlib.pyplot as plt
import time

# SDR Configuration
sample_rate = 1e6  # Sample rate in Hz
center_freq = 100e6  # Center frequency in Hz
capture_duration = 5  # Duration of capture in seconds

# Initialize the Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")  # Modify IP if necessary
sdr.rx_lo = int(center_freq)  # Set center frequency
sdr.sample_rate = int(sample_rate)  # Set sample rate
sdr.rx_rf_bandwidth = int(sample_rate)  # Set receiver bandwidth
sdr.rx_buffer_size = int(sample_rate * capture_duration)  # Set buffer size based on capture duration

# Capture data
print("Starting data capture...")
time.sleep(1)  # Allow SDR to stabilize
samples = sdr.rx()  # Receive samples from SDR
print("Data capture complete.")

# Time axis for plotting
time_axis = np.arange(len(samples)) / sample_rate  # Calculate time in seconds

# Plot time-domain signal (both I and Q components)
plt.figure(figsize=(12, 6))
plt.plot(time_axis, np.real(samples), label="In-phase (I)", color="blue")
plt.plot(time_axis, np.imag(samples), label="Quadrature (Q)", color="orange", alpha=0.7)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.title(f"Time Domain Signal (Capture Duration = {capture_duration}s)")
plt.grid()
plt.tight_layout()
plt.show()
