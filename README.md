import numpy as np
import adi
import matplotlib.pyplot as plt
from scipy import signal

# Initialize Pluto SDR
pluto = adi.Pluto('ip:192.168.2.1')

# Set up receiver parameters
sample_rate = 1e6  # 1 MS/s
center_freq = 433900000  # 433.9 MHz carrier frequency
gain_db = 50  # Set gain in dB
pluto.sample_rate = sample_rate
pluto.rx_lo = int(center_freq)
pluto.gain_control_mode_chan0 = 'slow_attack'
pluto.rx_hardwaregain_chan0 = gain_db

# Configure continuous reception
num_samps = int(sample_rate * 60)  # Collect data for 60 seconds
pluto.rx_buffer_size = num_samps

# Initialize arrays to store received samples
time = np.arange(num_samps) / sample_rate
samples = []

# Start receiving data
print("Starting data collection...")
for i in range(0, num_samps, pluto.rx_buffer_size):
    buffer = pluto.rx()
    samples.extend(buffer)

# Generate spectrogram
window = signal.hann(int(sample_rate))
nperseg = 1024
noverlap = 512
freqs, times, spectrogram = signal.spectrogram(np.array(samples), fs=sample_rate, nperseg=nperseg, noverlap=noverlap, window=window)

# Create spectrogram plot
plt.figure(figsize=(12, 8))
plt.imshow(spectrogram, aspect='auto', cmap='viridis', origin='lower')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.title('Spectrogram of Wireless Thermometer Transmission')
plt.colorbar(label='Power')
plt.show()

# Identify active transmission periods (you'll need to adjust these thresholds)
threshold = np.max(spectrogram) * 0.1
active_periods = []
for i in range(len(times) - 1):
    if spectrogram[i] > threshold and spectrogram[i+1] <= threshold:
        active_periods.append((times[i], times[i+1]))

print(f"Active transmission periods found: {active_periods}")

# Isolate signal for each active period
isolated_signals = []
for start_time, end_time in active_periods:
    idx_start = np.where(times >= start_time)[0][0]
    idx_end = np.where(times < end_time)[-1] + 1
    isolated_signal = samples[idx_start:idx_end]
    isolated_signals.append(isolated_signal)

# Plot magnitude and phase for each isolated signal
for i, sig in enumerate(isolated_signals):
    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.plot(sig)
    plt.title(f'Magnitude of Signal {i+1}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    
    plt.subplot(122)
    plt.plot(np.unwrap(np.angle(sig)))
    plt.title(f'Phase of Signal {i+1}')
    plt.xlabel('Sample')
    plt.ylabel('Phase (rad)')
    plt.tight_layout()
    plt.show()

# Determine modulation scheme (you'll need to analyze the plots)
# Based on observations, determine if it's AM, FM, PSK, QPSK, etc.

# Generate signal constellation diagram
for i, sig in enumerate(isolated_signals):
    plt.figure(figsize=(8, 8))
    plt.scatter(np.real(sig), np.imag(sig))
    plt.title(f'Signal Constellation Diagram {i+1}')
    plt.xlabel('In-phase')
    plt.ylabel('Quadrature')
    plt.tight_layout()
    plt.show()

# Analyze constellation diagram to determine modulation scheme
