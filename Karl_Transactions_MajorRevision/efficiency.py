import pandas as pd
import matplotlib.pyplot as plt
import io

# Configure matplotlib to use Times New Roman font for academic publishing
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman']
})

# 1. Raw data provided, cleaned for easy tab-separated parsing
raw_data = """Po	Pin	Efficiency	D	Load	Siemens
10	13.296	25.278	9.099451	230.4	0.004340278
20	23.871	56.480	12.868566	115.2	0.008680556
30	33.913	67.074	15.760711	76.8	0.013020833
40	44.406	72.554	18.198901	57.6	0.017361111
50	56.381	75.026	20.346990	46.08	0.021701389
60	65.961	76.972	22.289011	38.4	0.026041667
65	70.935	77.778	23.199138	35.44615385	0.028211806
70	77.562	78.545	24.074883	32.91428571	0.030381944
80	87.434	79.687	25.737133	28.8	0.034722222
90	97.945	80.548	27.298352	25.6	0.0390625
100	109.442	81.354	28.774989	23.04	0.043402778
110	118.536	81.888	30.179463	20.94545455	0.047743056
120	129.447	82.306	31.521421	19.2	0.052083333
130	140.450	82.742	32.808535	17.72307692	0.056423611
140	150.134	83.105	34.047026	16.45714286	0.060763889
150	159.694	83.316	35.242020	15.36	0.065104167
160	171.048	83.495	36.397802	14.4	0.069444444
170	181.608	83.703	37.517996	13.55294118	0.073784722
180	190.863	83.856	38.605699	12.8	0.078125
190	202.034	84.089	39.663585	12.12631579	0.082465278
200	211.414	84.125	40.693980	11.52	0.086805556
210	219.499	84.375	41.698921	10.97142857	0.091145833
220	232.160	84.457	42.680206	10.47272727	0.095486111
230	244.099	84.544	43.639432	10.0173913	0.099826389
240	251.724	84.699	44.578021	9.6	0.104166667"""

# 2. Load into a pandas DataFrame
df = pd.read_csv(io.StringIO(raw_data), sep='\t')

# 3. Plot Configuration (6x6 makes it a perfect square)
plt.figure(figsize=(6, 6))

# Plotting Converter Efficiency vs Input Power (Pin)
plt.plot(df['Pin'], df['Efficiency'], marker='o', linestyle='-', color='b', linewidth=2, markersize=5)

# 4. Graph Formatting (Academic Style)
plt.xlabel('Input Power (W)', fontsize=14)
plt.ylabel('Efficiency (%)', fontsize=14)
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

# Adjusting axes limits and ticks for a clean square layout
plt.xlim(0, 260)
plt.ylim(20, 100)
plt.xticks(range(0, 261, 40)) 
plt.yticks(range(20, 101, 10))

# 5. Save and Show
plt.tight_layout()
plt.savefig('efficiency_vs_pin_square.png', dpi=300) # Saves a high-res square image
plt.show()