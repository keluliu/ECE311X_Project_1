# Generate Spectrogram
def generate_spectrogram(iq_data, sampling_rate, fft_size):
    f, t, Sxx = spectrogram(iq_data, fs=sampling_rate, nperseg=fft_size, return_onesided=False)
    plt.figure()
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.colorbar(label='Intensity [dB]')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram of 433.9 MHz Transmission')
    plt.show()
