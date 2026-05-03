import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("plant0.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)

# Compute histograms
hist_h = cv2.calcHist([h], [0], None, [180], [0, 180])
hist_s = cv2.calcHist([s], [0], None, [256], [0, 256])
hist_v = cv2.calcHist([v], [0], None, [256], [0, 256])

# Normalize to range 0–1
hist_h = cv2.normalize(hist_h, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
hist_s = cv2.normalize(hist_s, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
hist_v = cv2.normalize(hist_v, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

# Plot
plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.plot(hist_h, color='m'); plt.title("Hue (normalized)")
plt.subplot(1,3,2); plt.plot(hist_s, color='g'); plt.title("Saturation (normalized)")
plt.subplot(1,3,3); plt.plot(hist_v, color='b'); plt.title("Value (normalized)")
plt.tight_layout()
plt.show()
