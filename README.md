sdr@ece331x:~$ /bin/python3 /home/sdr/Documents/ECE331X/ECE331X_Project_1/whetherSpectogram.py
Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/whetherSpectogram.py", line 91, in <module>
    samples = sdr.rx()
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/rx_tx.py", line 275, in rx
    data = self.__rx_complex()
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/rx_tx.py", line 240, in __rx_complex
    x = self._rx_buffered_data()
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/compat.py", line 149, in _rx_buffered_data
    self._rxbuf.refill()
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 1003, in refill
    _buffer_refill(self._buffer)
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 62, in _check_negative
    raise OSError(-result, _strerror(-result))
OSError: [Errno 27] File too large