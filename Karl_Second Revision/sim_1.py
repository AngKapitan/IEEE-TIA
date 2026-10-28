import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.ticker as ticker

# --- Configuration & Path Locking ---
if '__file__' in globals():
    base_dir = os.path.dirname(os.path.abspath(__file__))
else:
    base_dir = os.getcwd()

csv_file = os.path.join(base_dir, '100_48_240_PFC_zoom.csv')
# CHANGED: Output file is now a .pdf
output_pdf = os.path.join(base_dir, 'sim_plot_output.pdf')

# LaTeX-style math font settings for Matplotlib
plt.rcParams.update({
    "text.usetex": False, 
    "mathtext.fontset": "cm", 
    "font.family": "serif",
    "axes.labelsize": 22,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# --- Data Loading ---
if os.path.exists(csv_file):
    print(f"Found CSV at: {csv_file}")
    df = pd.read_csv(csv_file)
    df = df.apply(pd.to_numeric, errors='coerce').dropna() 
    
    time = df.iloc[:, 0]
    v_gs1 = df.iloc[:, 1] * 15  
    v_gs2 = df.iloc[:, 2] * 15
    i_lm1 = df.iloc[:, 3]
    i_lm2 = df.iloc[:, 4]
    b_o1 = df.iloc[:, 5]
    b_o2 = df.iloc[:, 6]
    b_c = df.iloc[:, 7]
else:
    print(f"ERROR: Could not find {csv_file}")
    print("Generating dummy data for demonstration...")
    time = np.linspace(0.428957, 0.428982, 500)
    v_gs1 = (np.sin(time * 1e6) > 0).astype(float) * 15
    v_gs2 = (np.cos(time * 1e6) > 0).astype(float) * 15
    i_lm1 = np.sin(time * 1e6) * 4 + 4
    i_lm2 = np.cos(time * 1e6) * 4 + 4
    b_o1 = np.sin(time * 1e6) * 0.1 + 0.1
    b_o2 = np.sin(time * 1e6) * 0.2
    b_c = np.cos(time * 1e6) * 0.1 + 0.1

# --- Figure Setup ---
fig, axs = plt.subplots(7, 1, figsize=(8, 10), sharex=True)
# Increased hspace slightly to leave room for the unit labels at the top of each axis
plt.subplots_adjust(hspace=0.25) 

# --- Shared Formatting Function ---
def format_axis(ax, ylabel, unit, ymin, ymax, yticks, yticklabels):
    ax.set_ylabel(ylabel, rotation=0, ha='right', va='center')
    ax.set_ylim(ymin, ymax)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.grid(True, which='both', linestyle=':', color='gray', alpha=0.6)
    
    # Hide top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add the unit at the tip of the Y-axis
    # (x=0.0 is the y-axis, y=1.05 is slightly above the top limit of the y-axis)
    ax.text(0.0, 1.05, unit, transform=ax.transAxes, ha='center', va='bottom', fontsize=8)

# --- Plot 1: Gate Signal 1 ---
axs[0].plot(time, v_gs1, color='blue', linewidth=2)
format_axis(axs[0], r'$v_{\mathrm{gs}_1}$', '[V]', -2, 17, [0, 15], ['0', '15'])

# --- Plot 2: Gate Signal 2 ---
axs[1].plot(time, v_gs2, color='red',  linewidth=2)
format_axis(axs[1], r'$v_{\mathrm{gs}_2}$', '[V]', -2, 17, [0, 15], ['0', '15'])

# --- Plot 3: Inductor Current 1 ---
axs[2].plot(time, i_lm1, color='blue', linewidth=2)
format_axis(axs[2], r'$i_{L_{\mathrm{m}_1}}$', '[A]', -2, 9, [0, 4, 8], ['0', '4', '8'])

# --- Plot 4: Inductor Current 2 ---
axs[3].plot(time, i_lm2, color='red', linewidth=2)
format_axis(axs[3], r'$i_{L_{\mathrm{m}_2}}$', '[A]', -2, 9, [0, 4, 8], ['0', '4', '8'])

# --- Plot 5: Outer Leg Flux 1 ---
axs[4].plot(time, b_o1, color='black', linewidth=2)
format_axis(axs[4], r'$B_{\mathrm{o}_1}$', '[T]', -0.1, 0.3, [0, 0.2], ['0', '0.2'])

# --- Plot 6: Outer Leg Flux 2 ---
axs[5].plot(time, b_o2, color='black', linewidth=2)
format_axis(axs[5], r'$B_{\mathrm{o}_2}$', '[T]', -0.3, 0.3, [-0.2, 0, 0.2], ['-0.2', '0', '0.2'])

# --- Plot 7: Center Leg Flux ---
axs[6].plot(time, b_c, color='black', linewidth=2)
format_axis(axs[6], r'$B_{\mathrm{c}}$', '[T]', -0.1, 0.3, [0, 0.2], ['0', '0.2'])

# --- X-Axis Formatting ---
axs[-1].set_xlim(0.428957, 0.428982)
axs[-1].set_xlabel('time [s]', fontsize=12)
axs[-1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%.5f'))

# Align the Y-axis labels
fig.align_ylabels(axs)

# --- Export ---
# CHANGED: format='pdf' and using output_pdf variable
plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
print(f"Successfully saved figure to {output_pdf}")