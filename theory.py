import math

# --- 1. Defined Parameters (From Table III) ---
AP_conv_single = 14128.75  # mm^4 (Area Product for ONE conventional core)
AP_integ       = AP_conv_single * 2  # mm^4 (Area Product for the proposed integrated core)
x              = 1.0       # Geometric ratio (Ac / Aw)
Ku             = 0.3       # Window occupancy ratio

# --- 2. Core Volume Computation (Proxy for Theoretical Core Loss) ---
# Shape factor function: f(x) = 2*x^(1/4) + x^(3/4) + x^(-1/4)
shape_factor = 2 * (x**0.25) + (x**0.75) + (x**-0.25)

# Vol = 2 * AP^(3/4) * f(x)
Vol_core_conv_single = 2 * (AP_conv_single**0.75) * shape_factor
Vol_core_conv_total  = 2 * Vol_core_conv_single  # Sum of two discrete cores

Vol_core_integ = 2 * (AP_integ**0.75) * shape_factor

# Core Loss Reduction Percentage
core_loss_reduction = (1 - (Vol_core_integ / Vol_core_conv_total)) * 100

# --- 3. Winding Volume Computation (Proxy for Theoretical Winding Loss) ---
# Ac = sqrt(x * AP) | Aw = sqrt(AP / x)
Ac_conv = math.sqrt(x * AP_conv_single)
Aw_conv = math.sqrt(AP_conv_single / x)

Ac_integ = math.sqrt(x * AP_integ)
Aw_integ = math.sqrt(AP_integ / x)

# Mean Length of Turn (MLT) is proportional to the center leg perimeter
# Assuming a square center leg, Perimeter = 4 * sqrt(Ac)
MLT_conv  = 4 * math.sqrt(Ac_conv)
MLT_integ = 4 * math.sqrt(Ac_integ)

# Vol_cu = Ku * Aw * MLT
Vol_cu_conv_single = Ku * Aw_conv * MLT_conv
Vol_cu_conv_total  = 2 * Vol_cu_conv_single  # Sum of copper on two discrete cores

Vol_cu_integ = Ku * Aw_integ * MLT_integ

# Winding Loss Reduction Percentage
cu_loss_reduction = (1 - (Vol_cu_integ / Vol_cu_conv_total)) * 100

# --- 4. Console Output ---
print("--- THEORETICAL COMPARISON (x = 1) ---\n")

print("1. CORE VOLUME (Proxy for Core Loss):")
print(f"   Conventional (2 cores): {Vol_core_conv_total:.2f} mm^3")
print(f"   Integrated (1 core):    {Vol_core_integ:.2f} mm^3")
print(f"   -> Core Loss Reduction: {core_loss_reduction:.2f}%\n")

print("2. COPPER VOLUME (Proxy for Winding Loss):")
print(f"   Conventional (2 cores): {Vol_cu_conv_total:.2f} mm^3")
print(f"   Integrated (1 core):    {Vol_cu_integ:.2f} mm^3")
print(f"   -> Winding Loss Reduction: {cu_loss_reduction:.2f}%\n")