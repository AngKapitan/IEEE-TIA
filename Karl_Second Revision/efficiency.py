import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.ticker as ticker

# --- Configuration & Path Locking ---
if '__file__' in globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
else:
    base_dir = os.getcwd()

output_pdf = os.path.join(base_dir, 'Efficiency_Curve_Rescaled.pdf')

# LaTeX-style math font settings for Matplotlib
plt.rcParams.update({
    "text.usetex": False, 
    "mathtext.fontset": "cm", 
    "font.family": "serif",
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

# --- Data Extraction[cite: 19] ---
# 25 data points corresponding to 10W increments up to 250W
input_power = np.arange(10, 260, 10)
efficiency = [
    25.278, 56.480, 67.074, 72.554, 75.026, 
    76.972, 77.778, 78.545, 79.687, 80.548, 
    81.354, 81.888, 82.306, 82.742, 83.105, 
    83.316, 83.495, 83.703, 83.856, 84.089, 
    84.125, 84.375, 84.457, 84.544, 84.699
]

# --- Figure Setup ---
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the efficiency curve with IEEE-style formatting[cite: 18]
ax.plot(input_power, efficiency, marker='o', markersize=6, color='blue', linewidth=2, label='Measured Efficiency')

# --- Axis Formatting ---
ax.set_xlabel('Input Power (W)')
ax.set_ylabel('Efficiency (%)')

# Tighter Y-axis range to improve readability as requested by the reviewer
ax.set_ylim(20, 90)
ax.set_xlim(0, 270)

ax.set_yticks(np.arange(20, 95, 10))
ax.set_xticks(np.arange(0, 261, 40))

# Clean grid formatting
ax.grid(True, which='major', linestyle='--', color='gray', alpha=0.5)

# Hide top and right spines for a cleaner academic look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# --- Export ---
plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
print(f"Successfully saved rescaled efficiency figure to {output_pdf}")