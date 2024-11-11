Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/spectrogram.py", line 121, in <module>
    generate_spectrogram(iq_data, sampling_rate, fft_size)
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/spectrogram.py", line 70, in generate_spectrogram
    f, t, Sxx = spectrogram(iq_data[:sampling_rate*10], fs=sampling_rate, nperseg=fft_size, return_onesided=False)  # Use a subset to avoid excessive memory use
  File "/home/sdr/.local/lib/python3.10/site-packages/numpy/_core/memmap.py", line 349, in __getitem__
    res = super().__getitem__(index)
TypeError: slice indices must be integers or None or have an __index__ method