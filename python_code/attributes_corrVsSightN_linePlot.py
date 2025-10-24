import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
segc_d = pd.read_csv('data/seth_environmentalGenusCountData_nov2024.csv')

segc_d.columns = segc_d.columns.str.strip()          # remove leading/trailing spaces
segc_d.columns = segc_d.columns.str.replace(' ', '_') # replace internal spaces with underscores
segc_d.columns = segc_d.columns.str.replace('\n', '') # remove newlines if present

# Select environmental columns
env_cols = [
    'DO', 'pH', 'avg_WW', 'avg_Depth', 'pflow_Pool', 'pflow_Run', 'pflow_Riffle',
    'pbottom_Mud', 'pbottom_Sand', 'pbottom_SmGravel', 'pbottom_LgGravel',
    'pbottom_Cobble', 'pbottom_Boulder', 'pbottom_Bedrock',
    'pfloat_macrophytes', 'pfloat_wood', 'upstreamCumDA_km2',
    'slopePercent', 'avgMonthFlow_cfs', 'CV_flow', 'maxMonthFlow_cfs', 'minMonthFlow_cfs'
]

# Correlation with total fish and richness
corr_total = segc_d[env_cols + ['t_population']].corr()['t_population'][env_cols]
corr_rich = segc_d[env_cols + ['t_species']].corr()['t_species'][env_cols]

corr_segc_d = pd.DataFrame({
    'Attribute': env_cols,
    'Total Fish': corr_total.values,
    'Species Richness': corr_rich.values
}).melt(id_vars='Attribute', var_name='Metric', value_name='Correlation')

plt.figure(figsize=(12, 6))
sns.barplot(data=corr_segc_d, x='Attribute', y='Correlation', hue='Metric')
plt.xticks(rotation=45, ha='right')
plt.title('Correlation of Environmental Attributes with Fish Metrics', fontsize=14)
plt.axhline(0, color='gray', linestyle='--', lw=1)
plt.tight_layout()
plt.show()