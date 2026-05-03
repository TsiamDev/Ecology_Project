import cv2
import numpy as np
import os 
from glob import glob
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from skimage.measure import shannon_entropy

def image_entropy(img):
    # Convert to grayscale for entropy computation
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return shannon_entropy(gray)


# -----------------------------
# CONFIG
# -----------------------------
PLACEHOLDER = "images/5_1_2026/" # folder containing the day's images
INPUT_FOLDER = PLACEHOLDER + "original_plants"  # folder containing .jpg files
OUTPUT_FOLDER = PLACEHOLDER + "isolated_plants" # folder to save results

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# PROCESS ALL JPG IMAGES
# -----------------------------
img_id = 0
for IMG_PATH in glob(os.path.join(INPUT_FOLDER, "*.jpg")):

    filename = os.path.basename(IMG_PATH)
    name, _ = os.path.splitext(filename)

    print("Processing:", filename)

    # -----------------------------
    # LOAD IMAGE
    # -----------------------------
    img = cv2.imread(IMG_PATH)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Compute histograms
    hist_h = cv2.calcHist([h], [0], None, [180], [0,180]).ravel()
    hist_s = cv2.calcHist([s], [0], None, [256], [0,256]).ravel()

    # Smooth histograms
    hist_h_smooth = gaussian_filter1d(hist_h, sigma=3)
    hist_s_smooth = gaussian_filter1d(hist_s, sigma=3)

    # Find peaks
    peaks_h, _ = find_peaks(hist_h_smooth, distance=10, prominence=0.05 * hist_h_smooth.max())
    peaks_s, _ = find_peaks(hist_s_smooth, distance=10, prominence=0.05 * hist_s_smooth.max())

    print("Hue peaks at bins:", peaks_h)
    print("Saturation peaks at bins:", peaks_s)

    def compute_boundaries(peaks):
        peaks = np.sort(peaks)
        boundaries = [(peaks[i] + peaks[i+1]) // 2 for i in range(len(peaks)-1)]
        return boundaries

    bound_h = compute_boundaries(peaks_h)
    bound_s = compute_boundaries(peaks_s)
    print("Hue boundaries at bins:", bound_h)
    print("Saturation boundaries at bins:", bound_s)

    def ranges_from_boundaries(boundaries, max_value):
        boundaries = [0] + boundaries + [max_value]
        return [(boundaries[i], boundaries[i+1]) for i in range(len(boundaries)-1)]

    hue_ranges = ranges_from_boundaries(bound_h, 180)
    sat_ranges = ranges_from_boundaries(bound_s, 256)
    print("Hue ranges:", hue_ranges)
    print("Saturation ranges:", sat_ranges)

    # 1 mask for 1 cluster of detected pixels
    hue_masks = [cv2.inRange(h, int(low), int(high)-1) for (low, high) in hue_ranges]
    sat_masks = [cv2.inRange(s, int(low), int(high)-1) for (low, high) in sat_ranges]

    # Combine hue and saturation masks to get cluster masks
    cluster_masks = []
    for hm in hue_masks:
        for sm in sat_masks:
            cluster_masks.append(cv2.bitwise_and(hm, sm))

    # Visualize one cluster
    #result = cv2.bitwise_and(img, img, mask=cluster_masks[0])
    #cv2.imshow("Cluster 0", result)
    #cv2.waitKey(0)

    #"""
    entropies = []
    cluster_id = 0
    for hi, hmask in enumerate(hue_masks):
        for si, smask in enumerate(sat_masks):
            combined = cv2.bitwise_and(hmask, smask)
            seg = cv2.bitwise_and(img, img, mask=combined)
            H = image_entropy(seg)
            entropies.append((H, seg, cluster_id))
            #cv2.imshow(f"Cluster H{hi}_S{si}", seg)
            cluster_id += 1

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Sort by entropy descending
    entropies.sort(key=lambda x: x[0], reverse=False)
    entropies = [(H, seg, c_id) for (H, seg, c_id) in entropies if ((H > 1.75) and (H < 3))]  # filter out empty segments
    if(len(entropies) == 0):
        print("No good clusters found based on entropy.")
        continue
    print(len(entropies))
    for best_entropy, best_segment, cluster_id in entropies:
        print("Entropy:", best_entropy)
        print(cluster_id)
        #cv2.imshow(f"Best Cluster", best_segment)
        cv2.imwrite(OUTPUT_FOLDER + "/plant_isolated_" + str(img_id) + "_" + str(cluster_id) + ".jpg", best_segment)
    
    img_id += 1

cv2.waitKey(0)
cv2.destroyAllWindows()