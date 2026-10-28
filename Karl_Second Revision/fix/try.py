import cv2
import numpy as np

# 1. Load the original screenshot
# Make sure to use the ORIGINAL image_344727.png, not the processed one
img = cv2.imread(r'C:\Users\simup\Documents\GitHub\IEEE-TIA\Karl_Second Revision\fix\zoomin32.5.png')

# 2. Convert to HSV and Grayscale for accurate isolation
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

saturation = hsv[:, :, 1]

# 3. Define accurate masks
# Black/Dark Mask: Low saturation (not colorful) AND low brightness (darker than the light-gray grid)
mask_black = (saturation < 40) & (gray < 150)

# Color Mask: High saturation (captures the blue, green, pink, and orange traces)
mask_color = saturation > 40

# 4. Create isolated layers on pure white backgrounds
# This automatically removes the grid, as grid pixels fall into neither mask
layer_black = np.full_like(img, 255)  # Pure white canvas
layer_black[mask_black] = img[mask_black]

layer_color = np.full_like(img, 255)  # Pure white canvas
layer_color[mask_color] = img[mask_color]

# 5. Thicken ONLY the color layer
# A 2x2 kernel provides a gentler, cleaner thickening than a 3x3. 
# Change to (3, 3) if you need them even bolder.
kernel = np.ones((3, 3), np.uint8)

# In OpenCV, eroding a white-background image thickens the dark/colored lines
layer_color_thick = cv2.erode(layer_color, kernel, iterations=1)

# 6. Merge the layers flawlessly
# cv2.min compares the two layers pixel-by-pixel and keeps the darkest one.
# This perfectly overlays the thick colored traces and the original black traces without jagged edges.
final_img = cv2.min(layer_black, layer_color_thick)

# 7. Save the output
cv2.imwrite('32.5.png', final_img)

print("Processing complete. Saved as '3252W.png'.")