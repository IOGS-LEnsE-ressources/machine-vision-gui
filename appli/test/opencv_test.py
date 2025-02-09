import cv2
import matplotlib.pyplot as plt
import numpy as np


array = cv2.imread('../Basler/images/bricks2.jpg', cv2.IMREAD_GRAYSCALE)
histogram = cv2.calcHist([array], [0], None, [256], [0, 256])

alpha = 1
beta = -200
array = array.astype(np.float64)
array_2 = cv2.convertScaleAbs(array, alpha=alpha, beta=beta)

print(f'N min = {np.min(array_2)}')


histogram_2 = cv2.calcHist([array_2], [0], None, [256], [0, 256])

plt.figure()
# Create a range of values (0 to 255) for the x-axis
x = np.arange(256)
# Plot the histogram as bars
plt.bar(x, histogram[:,0], width=1, color='black')
plt.xlim([0, 256])  # Limits for the x-axis
plt.figure()
# Create a range of values (0 to 255) for the x-axis
x = np.arange(256)
# Plot the histogram as bars
plt.bar(x, histogram_2[:,0], width=1, color='black')
plt.xlim([0, 256])  # Limits for the x-axis
plt.show()

'''
plt.figure()
plt.imshow(array, cmap='gray')
plt.figure()
plt.imshow(array_2, cmap='gray')
plt.show()
'''