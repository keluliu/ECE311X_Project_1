import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import adi  # Importing pyadi-iio for ADALM Pluto support

# Pluto SDR Configuration
center_frequency = 433.9e6  # Center frequency in Hz (433.9 MHz)
sampling_rate = 500e3       # Reduced Sampling rate in Hz to reduce data load
chunk_duration = 5          # Duration in seconds for each chunk of data
total_duration = 30         # Total duration in seconds for capturing data
fft_size = 256              # Reduced FFT size for memory efficiency
buffer_size = 1024          # Smaller buffer size for capturing more samples

# Initialize Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")  # Adjust IP if needed
sdr.rx_rf_bandwidth = int(sampling_rate)
sdr.rx_lo = int(center_frequency)
sdr.rx_buffer_size = buffer_size

# Function to capture data in chunks
def capture_data_in_chunks(total_duration, chunk_duration, sdr, sampling_rate):
    num_chunks = total_duration // chunk_duration
    chunk_samples = int(sampling_rate * chunk_duration)
    captured_data = []

    print("Capturing data in chunks...")
    for i in range(num_chunks):
        print(f"Capturing chunk {i + 1} of {num_chunks}...")
        samples = sdr.rx()
        if len(samples) > chunk_samples:
            samples = samples[:chunk_samples]  # Limit to chunk size
        captured_data.extend(samples)

    iq_data = np.array(captured_data, dtype='complex64')
    print("Data capture complete.")
    return iq_data

# Generate Spectrogram
def generate_spectrogram(iq_data, sampling_rate, fft_size):
    f, t, Sxx = spectrogram(iq_data, fs=sampling_rate, nperseg=fft_size, return_onesided=False)
    plt.figure()
    plt.pcolormesh(t, f, 10 * np.log10(np.abs(Sxx) + 1e-12), shading='gouraud')  # Add small value to prevent log(0)
    plt.colorbar(label='Intensity [dB]')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram of 433.9 MHz Transmission')
    plt.show()

# Generate Time-Domain Plots for Magnitude and Phase
def time_domain_analysis(iq_data):
    magnitude = np.abs(iq_data)
    phase = np.angle(iq_data)

    # Plot magnitude
    plt.figure()
    plt.plot(magnitude)
    plt.title('Time Domain Magnitude')
    plt.xlabel('Sample Index')
    plt.ylabel('Magnitude')
    plt.grid()
    plt.show()

    # Plot phase
    plt.figure()
    plt.plot(phase)
    plt.title('Time Domain Phase')
    plt.xlabel('Sample Index')
    plt.ylabel('Phase (radians)')
    plt.grid()
    plt.show()

# Generate Constellation Diagram
def plot_constellation(iq_data):
    plt.figure()
    plt.scatter(iq_data.real, iq_data.imag, alpha=0.5)
    plt.title('Constellation Diagram')
    plt.xlabel('In-phase (I)')
    plt.ylabel('Quadrature (Q)')
    plt.grid()
    plt.show()

# Main Execution
if __name__ == "__main__":
    # Capture data in smaller chunks from Pluto SDR
    iq_data = capture_data_in_chunks(total_duration, chunk_duration, sdr, sampling_rate)

    # Process and visualize data
    generate_spectrogram(iq_data, sampling_rate, fft_size)
    time_domain_analysis(iq_data)
    plot_constellation(iq_data)
