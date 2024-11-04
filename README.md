sdr@ece331x:~$ /bin/python3 /home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py
Traceback (most recent call last):
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/context_manager.py", line 36, in __init__
    self._ctx = iio.Context(self.uri)
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 1328, in __init__
    self._context = _new_uri(_context.encode("ascii"))
  File "/home/sdr/.local/lib/python3.10/site-packages/iio.py", line 56, in _check_null
    raise OSError(err, _strerror(err))
OSError: [Errno 38] Function not implemented

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/sdr/Documents/ECE331X/ECE331X_Project_1/example.py", line 13, in <module>
    sdr = adi.Pluto("192.168.2.1")
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/rx_tx.py", line 734, in __init__
    rx_def.__init__(self, *args, **kwargs)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/rx_tx.py", line 653, in __init__
    shared_def.__init__(self, *args, **kwargs)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/rx_tx.py", line 603, in __init__
    context_manager.__init__(self, uri_ctx, self._device_name)
  File "/home/sdr/.local/lib/python3.10/site-packages/adi/context_manager.py", line 38, in __init__
    raise Exception("No device found")
Exception: No device found