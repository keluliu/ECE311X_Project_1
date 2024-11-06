# Define time axis
time_axis = np.arange(len(samples)) / sample_rate * 1000

# Plot time-domain signal with separate subplots
plt.figure(figsize=(12, 8))

# Plot Real Part
plt.subplot(2, 1, 1)
plt.plot(time_axis, samples.real, label="Real", color="blue")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal (Real Part)")
plt.legend()

# Plot Imaginary Part
plt.subplot(2, 1, 2)
plt.plot(time_axis, samples.imag, label="Imaginary", color="orange")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.title("Time-Domain Signal (Imaginary Part)")
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
