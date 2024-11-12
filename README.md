/home/sdr/.local/lib/python3.10/site-packages/scipy/signal/_spectral_py.py:1936: RuntimeWarning: overflow encountered in multiply
  result = np.conjugate(result) * result
/home/sdr/.local/lib/python3.10/site-packages/scipy/signal/_spectral_py.py:1936: RuntimeWarning: invalid value encountered in multiply
  result = np.conjugate(result) * result
/home/sdr/.local/lib/python3.10/site-packages/scipy/signal/_spectral_py.py:1938: RuntimeWarning: invalid value encountered in multiply
  result *= scale
/home/sdr/Documents/ECE331X/ECE331X_Project_1/spectrogram.py:73: RuntimeWarning: overflow encountered in cast
  Sxx = np.where(np.isfinite(Sxx) & (Sxx < 1e300), Sxx, 0)  # Replace NaNs, infinities, and very large values with 0 to prevent overflow