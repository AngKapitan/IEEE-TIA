import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.integrate as integrate

# ==========================================
# 1. Define Circuit & Geometric Parameters
# ==========================================
# Electrical
D = 0.4               # Duty cycle
Ts = 1/100e3          # Switching period in seconds (10 us)
B_max_prime = 0.20    # Peak flux density in Tesla
n = 3.0               # Turns ratio
Vo = 48.0             # Output voltage
Vin_max = 100.0 * math.sqrt(2)  # Maximum input voltage

# Geometric (From Table III & Theoretical Assumptions)
AP_conv_single = 14128.75  # mm^4 (Area Product for ONE conventional core)
AP_integ       = AP_conv_single * 2  # mm^4 (Area Product for proposed integrated core)
x              = 1       # Geometric ratio (Ac / Aw)
Ku             = 0.3       # Window occupancy ratio

# ==========================================
# 2. Theoretical Volume Computation
# ==========================================
shape_factor = 2 * (x**0.25) + (x**0.75) + (x**-0.25)

# Conventional Volumes
Vol_core_conv_single = 2 * (AP_conv_single**0.75) * shape_factor
Vol_core_conv_total  = 2 * Vol_core_conv_single  # Sum of two discrete cores in mm^3

# Integrated Volumes
Vol_core_integ = 2 * (AP_integ**0.75) * shape_factor

# Subdivide Integrated Core into Center and Outer sections based on geometry
Ac_integ = math.sqrt(x * AP_integ)
Aw_integ = math.sqrt(AP_integ / x)

# Center leg volume = Ac * window_height
Vol_center_mm3 = Ac_integ * math.sqrt(Aw_integ)
# Yokes and outer legs split equally between the two outer phases
Vol_outer1_mm3 = (Vol_core_integ - Vol_center_mm3) / 2.0
Vol_outer2_mm3 = Vol_outer1_mm3

# Convert mm^3 to m^3 for absolute loss calculation
m3_conversion = 1e-9
Vol_core_conv_total_m3 = Vol_core_conv_total * m3_conversion
Vol_center_m3 = Vol_center_mm3 * m3_conversion
Vol_outer1_m3 = Vol_outer1_mm3 * m3_conversion
Vol_outer2_m3 = Vol_outer2_mm3 * m3_conversion

# ==========================================
# 3. Define Time Intervals (t1 to t7)
# ==========================================
t1 = 0.0
t2 = Vin_max * D * Ts / (n *Vo) + Ts * (D-0.5) + t1          
t3 = D * Ts + t1                
t4 = 0.5 * Ts + t1          
t5 = Vin_max * D * Ts / (n *Vo) + D * Ts + t1     
t6 = (0.5 + D) * Ts + t1           
t7 = 1.0 * Ts + t1           

t_int1 = np.linspace(t1, t2, 100, endpoint=False)
t_int2 = np.linspace(t2, t3, 100, endpoint=False)
t_int3 = np.linspace(t3, t4, 100, endpoint=False)
t_int4 = np.linspace(t4, t5, 100, endpoint=False)
t_int5 = np.linspace(t5, t6, 100, endpoint=False)
t_int6 = np.linspace(t6, t7, 100, endpoint=True)

t_total = []
B_prime = []
B_double_prime = []
B_o1 = []
B_o2 = []
B_c = []

# ==========================================
# 4. Calculate Equations per Interval
# ==========================================
# Interval 1
t_total.extend(t_int1)
for t in t_int1:
    bp = (B_max_prime / (D * Ts)) * t
    bdp = (-B_max_prime * n * Vo / (Vin_max * D * Ts)) * t + B_max_prime * (1 - (n * Vo / (Vin_max * D)) * (0.5 - D))
    bo1 = bp + bdp
    bo2 = bdp - bp
    bc = bdp
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

# Interval 2
t_total.extend(t_int2)
for t in t_int2:
    bp = (B_max_prime / (D * Ts)) * t
    bdp = 0.0
    bo1 = bp
    bo2 = -bp
    bc = 0.0
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

# Interval 3
t_total.extend(t_int3)
for t in t_int3:
    bp = (-B_max_prime * n * Vo / (Vin_max * D * Ts)) * t + B_max_prime * (1 + (n * Vo / Vin_max))
    bdp = 0.0
    bo1 = bp
    bo2 = -bp
    bc = 0.0
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

# Interval 4
t_total.extend(t_int4)
for t in t_int4:
    bp = (-B_max_prime * n * Vo / (Vin_max * D * Ts)) * t + B_max_prime * (1 + (n * Vo / Vin_max))
    bdp = (B_max_prime / (D * Ts)) * t - (0.5 * B_max_prime / D)
    bo1 = bp + bdp
    bo2 = bdp - bp
    bc = bdp
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

# Interval 5
t_total.extend(t_int5)
for t in t_int5:
    bp = 0.0
    bdp = (B_max_prime / (D * Ts)) * t - (0.5 * B_max_prime / D)
    bo1 = bdp
    bo2 = bdp
    bc = bdp
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

# Interval 6
t_total.extend(t_int6)
for t in t_int6:
    bp = 0.0
    bdp = (-B_max_prime * n * Vo / (Vin_max * D * Ts)) * t + B_max_prime * (1 + (n * Vo / (Vin_max * D)) * (0.5 + D))
    bo1 = bdp
    bo2 = bdp
    bc = bdp
    B_prime.append(bp)
    B_double_prime.append(bdp)
    B_o1.append(bo1)
    B_o2.append(bo2)
    B_c.append(bc)

t_total = np.array(t_total)
B_prime = np.array(B_prime)
B_double_prime = np.array(B_double_prime)
B_o1 = np.array(B_o1)
B_o2 = np.array(B_o2)
B_c = np.array(B_c)

# ==========================================
# 5. iGSE Core Loss Calculation
# ==========================================
# Steinmetz Parameters (Example for power ferrite at ~100kHz)
k_steinmetz = 12.0     
alpha = 1.30           
beta = 2.50            

# Calculate the iGSE constant (k_i)
def integrand(theta, a, b):
    return (abs(np.cos(theta))**a) * (abs(np.sin(theta))**(b - a))

integral_val, _ = integrate.quad(integrand, 0, 2*np.pi, args=(alpha, beta))
k_i = k_steinmetz / ( ((2*np.pi)**(alpha - 1)) * integral_val )

# Function to calculate iGSE loss density (Pv)
def calculate_igse_pv(t_arr, B_arr, ki, a, b, period):
    dt = np.diff(t_arr)
    dB = np.diff(B_arr)
    dt[dt == 0] = 1e-12 
    dBdt = dB / dt
    delta_b = np.max(B_arr) - np.min(B_arr)
    
    if delta_b == 0:
        return 0.0 
        
    integral_sum = np.sum((np.abs(dBdt)**a) * (delta_b**(b - a)) * dt)
    return (ki / period) * integral_sum

# Calculate volumetric power loss density (Pv) in W/m^3
# (Using B_double_prime strictly for the conventional discrete transformers)
Pv_conv = calculate_igse_pv(t_total, B_double_prime, k_i, alpha, beta, Ts)

Pv_o1 = calculate_igse_pv(t_total, B_o1, k_i, alpha, beta, Ts)
Pv_o2 = calculate_igse_pv(t_total, B_o2, k_i, alpha, beta, Ts)
Pv_c  = calculate_igse_pv(t_total, B_c, k_i, alpha, beta, Ts)

# ==========================================
# 6. Absolute Loss Integration & Output
# ==========================================
# Calculate absolute core loss in Watts
Loss_integ_o1 = Pv_o1 * Vol_outer1_m3
Loss_integ_o2 = Pv_o2 * Vol_outer2_m3
Loss_integ_c  = Pv_c * Vol_center_m3
Total_Integ_Loss = Loss_integ_o1 + Loss_integ_o2 + Loss_integ_c

# Conventional Loss strictly using the baseline B_double_prime waveform
Total_Conv_Loss = Pv_conv * Vol_core_conv_total_m3

# Reductions
core_vol_reduction = (1 - (Vol_core_integ / Vol_core_conv_total)) * 100
core_loss_reduction = (1 - (Total_Integ_Loss / Total_Conv_Loss)) * 100

print("--- 1. THEORETICAL VOLUME COMPARISON (x = 1) ---")
print(f"Conventional (2 cores): {Vol_core_conv_total:.2f} mm^3")
print(f"Integrated (1 core):    {Vol_core_integ:.2f} mm^3")
print(f"-> Volume Reduction:    {core_vol_reduction:.2f}%\n")

print("--- 2. iGSE CORE LOSS ANALYSIS ---")
print(f"Calculated k_i: {k_i:.5f}\n")

print(f"[Integrated Core Losses]")
print(f"Outer Leg 1 (Pv = {Pv_o1:8.2f} W/m^3) -> {Loss_integ_o1:.3f} W")
print(f"Outer Leg 2 (Pv = {Pv_o2:8.2f} W/m^3) -> {Loss_integ_o2:.3f} W")
print(f"Center Leg  (Pv = {Pv_c:8.2f} W/m^3) -> {Loss_integ_c:.3f} W")
print(f"TOTAL Integrated Loss = {Total_Integ_Loss:.3f} W\n")

print(f"[Conventional Core Losses]")
print(f"TOTAL Conventional Loss (Pv = {Pv_conv:.2f} W/m^3, using B''(t)) = {Total_Conv_Loss:.3f} W\n")

print(f"-> Core Loss Reduction: {core_loss_reduction:.2f}%")

# ==========================================
# 7. Plot the Results
# ==========================================
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(t_total, B_prime, label="B'(t)", linewidth=2)
plt.plot(t_total, B_double_prime, label="B''(t)", linewidth=2, linestyle='--')
plt.title("Magnetic Flux Densities over One Switching Period")
plt.ylabel("Flux Density (T)")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t_total, B_o1, label="Bo1(t)", linewidth=2)
plt.plot(t_total, B_o2, label="Bo2(t)", linewidth=2)
plt.plot(t_total, B_c, label="Bc(t)", linewidth=2, linestyle=':')
plt.xlabel("Time (s)")
plt.ylabel("Flux Density (T)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()