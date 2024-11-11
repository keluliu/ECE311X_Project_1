import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import adi  # Importing pyadi-iio for ADALM Pluto support

# Pluto SDR Configuration
center_frequency = 433.9e6  # Center frequency in Hz (433.9 MHz)
sampling_rate = 1e6         # Sampling rate in Hz
fft_size = 1024             # FFT size for spectrogram
time_duration = 30          # Duration in seconds for capturing data
output_file = "captured_data.npy"  # File to store captured data

# Initialize Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")  # Adjust IP if needed
sdr.rx_rf_bandwidth = int(sampling_rate)
sdr.rx_lo = int(center_frequency)
sdr.rx_buffer_size = 2048  # Smaller buffer size to avoid memory issues

# Capture I/Q data and save to disk in chunks
def capture_data(duration, sdr, sampling_rate, output_file):
    num_samples = int(sampling_rate * duration)
    captured_data = []

    print("Capturing data...")
    with open(output_file, 'wb') as f:
        captured_samples = 0
        while captured_samples < num_samples:
            samples = sdr.rx()
            captured_samples += len(samples)
            captured_data.extend(samples)
            
            # Save to file in chunks to avoid memory issues
            if len(captured_data) >= sdr.rx_buffer_size:
                np.save(f, np.array(captured_data[:sdr.rx_buffer_size], dtype='complex64'))
                captured_data = captured_data[sdr.rx_buffer_size:]  # Keep only remaining data in memory
            print(f"Captured {captured_samples} / {num_samples} samples")
    
    # Final write for remaining samples
    if len(captured_data) > 0:
        np.save(f, np.array(captured_data, dtype='complex64'))
    print("Data capture complete and saved to file.")

# Load data using memory-mapped file
def load_data(file_path):
    return np.memmap(file_path, dtype='complex64', mode='r')

# Generate Spectrogram
def generate_spectrogram(iq_data, sampling_rate, fft_size):
    subset_size = int(sampling_rate * 10)
    iq_data_subset = iq_data[:subset_size]  # Ensure the subset size is an integer
    f, t, Sxx = spectrogram(iq_data_subset, fs=sampling_rate, nperseg=fft_size, return_onesided=False)
    plt.figure()
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
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
    # Capture data from Pluto SDR
    capture_data(time_duration, sdr, sampling_rate, output_file)
    
    # Load captured data
    iq_data = load_data(output_file)
    
    # Process and visualize data
    generate_spectrogram(iq_data, sampling_rate, fft_size)
    time_domain_analysis(iq_data)
    plot_constellation(iq_data)
