from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

figsize = (7, 6.8)
dpi = 100
ylims = (-3, 3)

data_root = Path(__file__).parent.parent / 'data'

# load swe data
ea = pd.read_csv(
    data_root / 'ARC_SWE_std_output_ea.csv',
    names=['year', 'april_swe_ea', 'april_swe_ea_min', 'april_swe_ea_max'],
    dtype={
        'year': int,
        'april_swe_ea': float,
        'april_swe_ea_min': float,
        'april_swe_ea_max': float
    }
).set_index('year', drop=True)
na = pd.read_csv(
    data_root / 'ARC_SWE_std_output_na.csv',
    names=['year', 'april_swe_na', 'april_swe_na_min', 'april_swe_na_max'],
    dtype={
        'year': int,
        'april_swe_na': float,
        'april_swe_na_min': float,
        'april_swe_na_max': float
    }
).set_index('year', drop=True)
df = pd.merge(left=na, right=ea, left_index=True, right_index=True)

# initialize canvas
fig, ax = plt.subplots(figsize=figsize)
# setting margins
plt.subplots_adjust(top=0.95, bottom=0.11, left=0.12, right=0.95)
# forcing inner-ticks
ax.tick_params(axis='both', direction='in', top=True, right=True)
# increase x-axis ticklabel pad a bit
[tick.set_pad(13) for tick in ax.xaxis.get_major_ticks()]
ax.xaxis.labelpad = 8

# plot empty circles
df[['april_swe_na', 'april_swe_ea']].plot(
    ax=ax, linestyle='None', linewidth=0.1, zorder=2, marker='o', 
    markerfacecolor='None', markersize=10, legend=False, color=['black', 'red']
)
# plot "latest year" filled circles
latest_year = df.index.max()
current = df.loc[[latest_year]]
current['april_swe_na'].plot(
    ax=ax, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='black', markersize=10, legend=False, color='black'
)
current['april_swe_ea'].plot(
    ax=ax, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='red', markersize=10, legend=False, color='black'
)

# plot 5-year mean raw anomaly and fill-betweens
sub = df.set_index(
    pd.date_range(f'{df.index.min()}-01-01', f'{df.index.max()}-01-01', freq='YS')
)
# NB: swapped order for the raw mean so it plots NA overtop of EA
rolling_raw = sub[['april_swe_ea','april_swe_na']].rolling(5, min_periods=0, closed='both', center=True).mean()
rolling_max = sub[['april_swe_na_max', 'april_swe_ea_max']].rolling(5, min_periods=0, closed='both', center=True).mean()
rolling_min = sub[['april_swe_na_min', 'april_swe_ea_min']].rolling(5, min_periods=0, closed='both', center=True).mean()
rolling_raw.set_index(rolling_raw.index.year).plot(
    ax=ax, solid_joinstyle='round', legend=False, 
    zorder=1, linewidth=3, color=['red', 'black']
)
# north america fillbetween
ax.fill_between(
    df.index, 
    y1=rolling_min['april_swe_na_min'].values, 
    y2=rolling_max['april_swe_na_max'].values,
    facecolor='black',
    alpha=0.2
)
# eurasia fillbetween
ax.fill_between(
    df.index, 
    y1=rolling_min['april_swe_ea_min'].values, 
    y2=rolling_max['april_swe_ea_max'].values,
    facecolor='red',
    alpha=0.2
)

# axis formatting
xmin = df.index.min()-1 
xmax = df.index.max()+1
ax.set_ylabel('April SWE Anomaly')
ax.set_xlabel('Year')
ax.set_ylim(ylims)
ax.set_xlim(left=xmin, right=xmax)
ax.hlines([0], xmin=xmin, xmax=xmax, linestyles=(0,[8, 2]), zorder=5, edgecolor='black', linewidth=1, alpha=0.8)

# Add legend
na_marker = Line2D([0], [0], marker='o', color='None', markersize=10, markerfacecolor='black', label='North American Arctic')
ea_marker = Line2D([0], [0], marker='o', color='None', markersize=10, markerfacecolor='red', label='Eurasian Arctic')
ax.legend(handles=[na_marker, ea_marker], loc=2, fontsize=14, frameon=False)

# save
plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig4-python.png', dpi=dpi)
