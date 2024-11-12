import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import adi  # Importing pyadi-iio for ADALM Pluto support

# Pluto SDR Configuration
center_frequency = 433.9e6  # Center frequency in Hz (433.9 MHz)
sampling_rate = 1e6         # Sampling rate in Hz
fft_size = 512              # FFT size for spectrogram
time_duration = 10          # Duration in seconds for capturing data

# Initialize Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")  # Adjust IP if needed
sdr.rx_rf_bandwidth = int(sampling_rate)
sdr.rx_lo = int(center_frequency)
sdr.rx_buffer_size = 4096  # Buffer size for capturing more samples

# Capture I/Q data
def capture_data(duration, sdr, sampling_rate):
    num_samples = int(sampling_rate * duration)
    iq_data = np.zeros(num_samples, dtype='complex64')
    captured_samples = 0

    print("Capturing data...")
    while captured_samples < num_samples:
        samples = sdr.rx()  # Fetch samples from Pluto SDR
        remaining_samples = num_samples - captured_samples
        samples_to_store = min(len(samples), remaining_samples)
        iq_data[captured_samples:captured_samples + samples_to_store] = samples[:samples_to_store]
        captured_samples += samples_to_store
        print(f"Captured {captured_samples} / {num_samples} samples")
    
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
    # Capture data from Pluto SDR
    iq_data = capture_data(time_duration, sdr, sampling_rate)
    
    # Process and visualize data
    generate_spectrogram(iq_data, sampling_rate, fft_size)
    time_domain_analysis(iq_data)
    plot_constellation(iq_data)
