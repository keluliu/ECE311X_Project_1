sdr@ece331x:~$ /bin/python3 /home/sdr/Documents/ECE331X/ECE331X_Project_1/spectrogram.py
Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/spectrogram.py", line 105, in <module>
    sdr.rx_lo = int(center_freq)  # Set center frequency
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/ad936x.py", line 197, in rx_lo
    self._set_iio_attr_int("altvoltage0", "frequency", True, value)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/attribute.py", line 94, in _set_iio_attr_int
    self._set_iio_attr(channel_name, attr_name, output, value, _ctrl)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/attribute.py", line 71, in _set_iio_attr
    raise ex
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/attribute.py", line 69, in _set_iio_attr
    channel.attrs[attr_name].value = str(value)
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 704, in <lambda>
    lambda self, x: self._write(x),
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 736, in _write
    _c_write_attr(self._channel, self._name_ascii, value.encode("ascii"))
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 62, in _check_negative
    raise OSError(-result, _strerror(-result))
OSError: [Errno 22] Invalid argument