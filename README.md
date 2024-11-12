import adi  # Analog Devices ADI Python library for PlutoSDR
import numpy as np
import time

# Initialize PlutoSDR
sdr = adi.Pluto("ip:192.168.2.1")

# SDR Configuration
sample_rate = 1e6  # Hz
center_freq = 100e6  # Center frequency in Hz
duration = 10  # Duration to receive data in seconds

# SDR Settings
sdr.rx_lo = int(center_freq)  # Set center frequency
sdr.sample_rate = int(sample_rate)  # Set sample rate
sdr.rx_rf_bandwidth = int(sample_rate)  # Set bandwidth
sdr.rx_buffer_size = 1024  # Set buffer size (number of samples per read)

# Start receiving data
start_time = time.time()
all_data = []  # List to store all received data

print("Receiving data...")
while time.time() - start_time < duration:
    samples = sdr.rx()  # Receive samples
    all_data.append(samples)

# Convert list of arrays to a single array
all_data = np.concatenate(all_data)

print("Data received for", duration, "seconds.")
print("Total samples received:", len(all_data))
