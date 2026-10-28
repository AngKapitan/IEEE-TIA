import matplotlib.pyplot as plt
import numpy as np
import os

# --- Configuration & Path Locking ---
if '__file__' in globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
else:
    base_dir = os.getcwd()

output_pdf = os.path.join(base_dir, 'Efficiency_Curve_40W_to_250W.pdf')

# LaTeX-style math font settings for Matplotlib
plt.rcParams.update({
    "text.usetex": False, 
    "mathtext.fontset": "cm", 
    "font.family": "serif",
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

# --- Data Extraction ---
# Slicing the arrays to start from the 4th data point (40 W)
input_power = np.arange(10, 260, 10)[3:] 
efficiency = [
    25.278, 56.480, 67.074, 72.554, 75.026, 
    76.972, 77.778, 78.545, 79.687, 80.548, 
    81.354, 81.888, 82.306, 82.742, 83.105, 
    83.316, 83.495, 83.703, 83.856, 84.089, 
    84.125, 84.375, 84.457, 84.544, 84.699
][3:]

# --- Figure Setup ---
fig, ax = plt.subplots(figsize=(8, 5))

# Plot the efficiency curve
ax.plot(input_power, efficiency, marker='o', markersize=6, color='blue', linewidth=2, label='Measured Efficiency')

# --- Axis Formatting ---
ax.set_xlabel('Input Power (W)')
ax.set_ylabel('Efficiency (%)')

# Tighter Y-axis range to explicitly address the reviewer's complaint
ax.set_ylim(70, 86)
ax.set_xlim(30, 260)

# Set ticks for clean intervals
ax.set_yticks(np.arange(70, 86, 5))
ax.set_xticks(np.arange(30, 270, 30))

# Clean grid formatting
ax.grid(True, which='major', linestyle='--', color='gray', alpha=0.5)

# Hide top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# --- Export ---
plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
print(f"Successfully saved 40W+ efficiency figure to {output_pdf}")