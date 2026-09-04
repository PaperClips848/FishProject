import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

from matplotlib import colormaps
list(colormaps)

# === Load Data ===
data = pd.read_csv('data/seth_environmentalGenusCountData_nov2024.csv')

data = data.drop(columns=['SiteN','State','Lat','Long', 'Ameiurus','Aphredoderus','Aplodinotus','Campostoma','Cyprinella','Cyprinus','Dorosoma','Ellasoma','Erimyzon','Esox','Etheostoma','Fundulus','Gambusia','Ictalurus','Labidesthes','Lepisosteus','Lepomis','Lythrus','Macrohybopsis','Micropterus','Minytrema','Moxostoma','Nototropis','Notemigonus','Notropis','Noturus','Percina','Phenocobius','Pimephales','Semotilus'])

# === Compute correlation matrix ===
c_m = data.corr(numeric_only=True)

# === Ensure output folder exists ===
os.makedirs("../figures", exist_ok=True)

# === Plot and save ===
plt.figure(figsize=(12, 10))
sns.heatmap(c_m, cmap="flare", annot=False)
plt.title("Correlation Heatmap of Environmental & Genus Data")

# Save the figure
plt.tight_layout()
plt.show("figures/correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()  # ensures the figure is finalized and file is written

print("✅ Heatmap saved to figures/correlation_heatmap.png")