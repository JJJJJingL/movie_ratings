import numpy as np

data = [1, 2, 3, 4, 5, 6]
q75, q25 = np.percentile(data, [75,25])
print(q75, q25)