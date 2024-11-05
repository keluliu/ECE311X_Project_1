sdr@ece331x:~$ /bin/python3 /home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py
Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py", line 78, in <module>
    sdr.rx_rf_bandwidth = 433e6  # Set bandwidth
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/ad936x.py", line 83, in rx_rf_bandwidth
    self._set_iio_attr_int("voltage0", "rf_bandwidth", False, value)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/attribute.py", line 93, in _set_iio_attr_int
    raise Exception("Value must be an int")
Exception: Value must be an int