sdr@ece331x:~$ /bin/python3 /home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py
Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py", line 19, in <module>
    sdr.sample_rate = 433.9*10**6*2
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/ad936x.py", line 187, in sample_rate
    self._set_iio_attr("voltage0", "sampling_frequency", False, rate)
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