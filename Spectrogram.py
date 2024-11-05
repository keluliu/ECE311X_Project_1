# import iio
# import adi
# import numpy as np
# import sys

# sdr = adi.Pluto("ip:192.168.2.1")
# rx_rf_bandwidth = 433000000
# data = sdr.rx()
# np.set_printoptions(threshold=sys.maxsize)
# print(data)

import time
import adi
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Constants
CARRIER_FREQUENCY = 433.9e6  # Carrier frequency in Hz
SAMPLE_RATE = 6e6  # Sampling rate in Hz
COLLECTION_DURATION = 60  # Total duration for data collection in seconds
INTERMITTENT_INTERVAL = 15  # Time interval between transmissions in seconds

# Create SDR instance
sdr = adi.Pluto("ip:192.168.2.1")

# Configure SDR
sdr.sample_rate = SAMPLE_RATE
sdr.rx_rf_bandwidth = 4e6  # Set bandwidth
sdr.rx_lo = CARRIER_FREQUENCY  # Set LO frequency

# Initialize an empty list to store the collected data
data_buffer = []

# Collect data
start_time = time.time()
while time.time() - start_time < COLLECTION_DURATION:
    # Check if we should collect data
    current_time = time.time()
    if int(current_time) % INTERMITTENT_INTERVAL == 0:
        print(f"Collecting data at {time.ctime(current_time)}...")
        x = sdr.rx()  # Receive data
        data_buffer.extend(x)  # Append received data to buffer
        time.sleep(INTERMITTENT_INTERVAL)  # Wait for the next interval

# Convert collected data to a NumPy array
data_array = np.array(data_buffer)

# Generate Spectrogram
frequencies, times, Sxx = signal.spectrogram(data_array, fs=SAMPLE_RATE)

# Plot the Spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram of Wireless Transmission')
plt.colorbar(label='Intensity [dB]')
plt.ylim([0, 1e6])  # Adjust frequency limits as needed
plt.show()
