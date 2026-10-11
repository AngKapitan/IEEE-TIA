import cv2
import numpy as np
import sys

# 1. Load the original screenshot (Using relative path so it doesn't crash)
img = cv2.imread('zoomin240.png')

if img is None:
    print("Error: Could not find 'zoomin32.5.png'. Make sure it is in the same folder as this script!")
    sys.exit()

# 2. Convert to HSV and Grayscale
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
saturation = hsv[:, :, 1]

# 3. Define accurate masks
mask_black = (saturation < 40) & (gray < 150)
mask_color = saturation > 40

# Create a proper 0-or-255 format mask for the black traces for computer vision analysis
mask_black_uint8 = (mask_black * 255).astype(np.uint8)

# 4. Create the base layers (White canvases)
layer_black = np.full_like(img, 255)
layer_black[mask_black] = img[mask_black]

layer_color = np.full_like(img, 255)
layer_color[mask_color] = img[mask_color]

# 5. Thicken the COLOR layers aggressively
kernel_heavy = np.ones((3, 3), np.uint8)
# Erode on a white background makes the colored lines thicker
layer_color_thick = cv2.erode(layer_color, kernel_heavy, iterations=1)

# =========================================================================
# 6. ISOLATE AND THICKEN ONLY THE WAVY C1 TRACE (END TO END)
# =========================================================================

# Process the entire image width (no more x_start or x_end limits!)
roi_mask = mask_black_uint8.copy()

# Step A: Break the grid web
kernel_vert = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
vertical_lines = cv2.morphologyEx(roi_mask, cv2.MORPH_OPEN, kernel_vert)
roi_broken_web = cv2.subtract(roi_mask, vertical_lines)

# Step B: Connected components on the entire image
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(roi_broken_web, connectivity=8)

trace_only_mask = np.zeros_like(roi_broken_web)

for i in range(1, num_labels):
    width = stats[i, cv2.CC_STAT_WIDTH]
    height = stats[i, cv2.CC_STAT_HEIGHT]
    
    # 1. Grid dashes are tiny (width < 20).
    # 2. Channel separators are perfectly flat (height < 5).
    # 3. Text labels and boxes (like "C1") are small (width < 100).
    # 4. The actual C1 trace is massive (width > 150) AND fluctuates (height > 5).
    if width > 150 and height > 5:  
        trace_only_mask[labels == i] = 255

# Thicken ONLY the isolated C1 trace
trace_only_mask_thick = cv2.dilate(trace_only_mask, kernel_heavy, iterations=1)

final_black = layer_black.copy()

# Paint the thick C1 trace back onto the entire image, end to end!
final_black[trace_only_mask_thick == 255] = (0, 0, 0)

# =========================================================================
# 7. Merge and Save
# =========================================================================

# Merge the modified black layer and the thickened color layer
final_img = cv2.min(final_black, layer_color_thick)

cv2.imwrite('240_thick.png', final_img)
print("Processing complete! Grid is thin, traces are thick. Saved as '32.5_thick.png'.")