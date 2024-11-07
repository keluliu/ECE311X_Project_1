import adi
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal

# Constants
CARRIER_FREQUENCY = int(433.9e6)  # Carrier frequency in Hz
SAMPLE_RATE = int(6e6)  # Sampling rate in Hz
COLLECTION_DURATION = 30  # Total duration for data collection in seconds
INTERMITTENT_INTERVAL = 15  # Time interval between transmissions in seconds
FFT_SIZE = 1024  # Size of FFT for spectrogram

# Create SDR instance
sdr = adi.Pluto("ip:192.168.2.1")

# Configure SDR
sdr.sample_rate = SAMPLE_RATE
sdr.rx_rf_bandwidth = int(4e6)  # Set bandwidth to 4 MHz
sdr.rx_lo = CARRIER_FREQUENCY  # Set LO frequency to 433.9 MHz

# Print out the configured properties to verify
print(f"Sample Rate: {sdr.sample_rate}")
print(f"RX LO: {sdr.rx_lo}")

# Initialize an empty list to store the collected data
data_buffer = []

# Collect data
start_time = time.time()
while time.time() - start_time < COLLECTION_DURATION:
    current_time = time.time()
    if int(current_time) % INTERMITTENT_INTERVAL == 0:
        print(f"Collecting data at {time.ctime(current_time)}...")
        x = sdr.rx()  # Receive data
        data_buffer.extend(x)  # Append received data to buffer
        time.sleep(INTERMITTENT_INTERVAL)  # Wait for the next interval

# Convert collected data to a NumPy array
data_array = np.array(data_buffer)

# Define time axis
time_axis = np.arange(len(data_array)) / SAMPLE_RATE * 1000  # in ms

# Plot time-domain signal
plt.figure(figsize=(12, 6))
plt.plot(time_axis, data_array.real, label="Real", color="blue", alpha=0.5)
plt.plot(time_axis, data_array.imag, label="Imaginary", color="orange", alpha=0.5)
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal")
plt.legend()
plt.grid()
plt.xlim([0, 30])  # Set x-axis limit to focus on the desired time range
plt.ylim([-2500, 2500])  # Adjust y-axis limits as needed for visibility
plt.tight_layout()
plt.show()

# Generate Spectrogram
frequencies, times, Sxx = signal.spectrogram(data_array, fs=SAMPLE_RATE, nperseg=FFT_SIZE)

# Plot the Spectrogram
plt.figure(figsize=(12, 6))
plt.pcolormesh(times, frequencies / 1e6, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency [MHz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram of Wireless Transmission')
plt.colorbar(label='Intensity [dB]')
plt.ylim([0, 2])  # Limit frequency range for visibility, adjust as needed
plt.show()

