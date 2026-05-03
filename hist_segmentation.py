import cv2
import numpy as np

img = cv2.imread("plant0.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(hsv)

# Example peak ranges
hue_ranges = [(5, 15), (30, 40), (170, 180)]
sat_ranges = [(7, 12), (13, 17), (18, 22)]

hue_masks = []
for low, high in hue_ranges:
    mask = cv2.inRange(h, low, high)
    hue_masks.append(mask)

sat_masks = []
for low, high in sat_ranges:
    mask = cv2.inRange(s, low, high)
    sat_masks.append(mask)

segmented = cv2.bitwise_and(img, img, mask=hue_masks[0])
cv2.imshow("Segmented Peak 1", segmented)
cv2.waitKey(0)
