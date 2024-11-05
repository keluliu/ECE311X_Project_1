# Copyright (C) 2019-2024 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import iio


class context_manager(object):
    _uri_auto = "ip:analog"
    _ctx = None

    @property
    def ctx(self) -> iio.Context:
        """IIO Context"""
        return self._ctx

    def __init__(self, uri="", _device_name=""):
        if self._ctx:
            return
        self.uri = uri
        try:
            if self.uri == "":
                # Try USB contexts first
                if _device_name != "":
                    contexts = iio.scan_contexts()
                    for c in contexts:
                        if _device_name in contexts[c]:
                            self._ctx = iio.Context(c)
                            break
                # Try auto discover
                if not self._ctx and self._uri_auto != "":
                    self._ctx = iio.Context(self._uri_auto)
                if not self._ctx:
                    raise Exception("No device found")
            else:
                self._ctx = iio.Context(self.uri)
        except BaseException:
            raise Exception("No device found")

@keluliu ➜ /workspaces/ECE311X_Project_1 (main) $ /home/codespace/.python/current/bin/python3 /workspaces/ECE311X_Project_1/Spectrogram.py
Traceback (most recent call last):
  File "/home/codespace/.python/current/lib/python3.12/site-packages/adi/context_manager.py", line 36, in __init__
    self._ctx = iio.Context(self.uri)
                ^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.python/current/lib/python3.12/site-packages/iio.py", line 1328, in __init__
    self._context = _new_uri(_context.encode("ascii"))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.python/current/lib/python3.12/site-packages/iio.py", line 56, in _check_null
    raise OSError(err, _strerror(err))
TimeoutError: [Errno 110] Connection timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/workspaces/ECE311X_Project_1/Spectrogram.py", line 6, in <module>
    sdr = adi.Pluto("ip:192.168.2.1")
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/codespace/.python/current/lib/python3.12/site-packages/adi/rx_tx.py", line 734, in __init__
    rx_def.__init__(self, *args, **kwargs)
  File "/home/codespace/.python/current/lib/python3.12/site-packages/adi/rx_tx.py", line 653, in __init__
    shared_def.__init__(self, *args, **kwargs)
  File "/home/codespace/.python/current/lib/python3.12/site-packages/adi/rx_tx.py", line 603, in __init__
    context_manager.__init__(self, uri_ctx, self._device_name)
  File "/home/codespace/.python/current/lib/python3.12/site-packages/adi/context_manager.py", line 38, in __init__
    raise Exception("No device found")
Exception: No device found