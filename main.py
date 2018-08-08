import sys
print ('sys.version is', sys.version)
print('sys.path is', sys.path)

import numpy as np
a = np.arange(15).reshape(3, 5)
print('numpy seems to work:\n', a)

