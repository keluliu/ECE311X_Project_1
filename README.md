import numpy as np
from rtlsdr import RtlSdr

# Configure the SDR
sdr = RtlSdr()

sdr.sample_rate = 1e6  # Set the sample rate
sdr.center_freq = 433.9e6  # Set the center frequency
sdr.gain = 'auto'  # Automatic gain

# Collect data for 2 minutes (120 seconds)
duration = 120  # in seconds
samples = []

try:
    print("Collecting data...")
    samples = sdr.read_samples(duration * sdr.sample_rate)
    print("Data collection complete.")
finally:
    sdr.close()