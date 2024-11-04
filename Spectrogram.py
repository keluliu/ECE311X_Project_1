import iio
import adi
import numpy as np
import sys

sdr = adi.Pluto("ip:192.168.2.1")
rx_rf_bandwidth = 433000000
data = sdr.rx()
np.set_printoptions(threshold=sys.maxsize)
print(data)