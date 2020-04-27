from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

#### FLAG TO ASSIGN OUTPUT FIGURE FORMAT
FIG_FMT = 'PDF' # or 'PNG' or 'TIF'

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

figsize = (11, 5)
dpi = 200
ylims = (-4, 4)

data_root = Path(__file__).parent.parent / 'data'

# load sce data
ea = pd.read_csv(
    data_root / 'ARC_SCE_std_output_ea.csv',
    names=['year', 'may_sce_ea', 'june_sce_ea'],
    dtype={
        'year': int,
        'may_sce_ea': float,
        'june_sce_ea': float
    }
).set_index('year', drop=True)
na = pd.read_csv(
    data_root / 'ARC_SCE_std_output_na.csv',
    names=['year', 'may_sce_na', 'june_sce_na'],
    dtype={
        'year': int,
        'may_sce_na': float,
        'june_sce_na': float
    }
).set_index('year', drop=True)
df = pd.merge(left=na, right=ea, left_index=True, right_index=True)

# initialize canvas
fig, (ax_may, ax_june) = plt.subplots(
    figsize=figsize, ncols=2, nrows=1
)
# setting margins
plt.subplots_adjust(top=0.95, bottom=0.12, left=0.08, right=0.95, wspace=0.2, hspace=0.2)

# plot empty circles
df[['may_sce_na', 'may_sce_ea']].plot(
    ax=ax_may, linestyle='None', linewidth=0.1, zorder=2, marker='o', 
    markerfacecolor='white', markersize=10, legend=False, color=['black', 'red']
)
df[['june_sce_na', 'june_sce_ea']].plot(
    ax=ax_june, linestyle='None', linewidth=0.1, zorder=2, marker='o', 
    markerfacecolor='white', markersize=10, legend=False, color=['black', 'red']
)
# plot "latest year" filled circles
latest_year = df.index.max()
current = df.loc[[latest_year]]
current['may_sce_na'].plot(
    ax=ax_may, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='black', markersize=10, legend=False, color='black'
)
current['may_sce_ea'].plot(
    ax=ax_may, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='red', markersize=10, legend=False, color='black'
)
current['june_sce_na'].plot(
    ax=ax_june, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='black', markersize=10, legend=False, color='black'
)
current['june_sce_ea'].plot(
    ax=ax_june, linestyle='None', linewidth=0.1, zorder=3, marker='o', 
    markerfacecolor='red', markersize=10, legend=False, color='black'
)

# plot means
sub_mean = df.iloc[:-1]
sub_mean = sub_mean.set_index(
    pd.date_range(f'{sub_mean.index.min()}-01-01', f'{sub_mean.index.max()}-01-01', freq='YS')
)
rolling_may = sub_mean[['may_sce_na', 'may_sce_ea']].rolling(5, min_periods=0, closed='both', center=True).mean()
rolling_may.set_index(rolling_may.index.year).plot(
    ax=ax_may, solid_joinstyle='round', legend=False, 
    zorder=1, linewidth=3, color=['black', 'red']
)
rolling_june = sub_mean[['june_sce_na', 'june_sce_ea']].rolling(5, min_periods=0, closed='both', center=True).mean()
rolling_june.set_index(rolling_june.index.year).plot(
    ax=ax_june, solid_joinstyle='round', legend=False, 
    zorder=1, linewidth=3, color=['black', 'red']
)

# axes formatting
xmin = df.index.min()-1 
xmax = df.index.max()+1
for ax in [ax_may, ax_june]:
    ax.set_xlabel('Year')
    ax.set_ylim(ylims)
    ax.set_xlim(left=xmin, right=xmax)
    ax.hlines([0], xmin=xmin, xmax=xmax, linestyles=(0,[8, 2]), zorder=5, edgecolor='black', linewidth=1, alpha=0.8)
ax_may.set_ylabel('May SCE Anomaly')
ax_june.set_ylabel('June SCE Anomaly')

# Add legend
na_marker = Line2D([0], [0], marker='o', color='None', markersize=10, markerfacecolor='black', label='North American Arctic')
ea_marker = Line2D([0], [0], marker='o', color='None', markersize=10, markerfacecolor='red', label='Eurasian Arctic')
ax_may.legend(handles=[na_marker, ea_marker], loc=3, fontsize=12, frameon=False)

# axis text indicators
#ax_may.text(0.02, 0.92, 'a.', fontsize=20, transform=ax_may.transAxes)
ax_may.text(-0.15, 0.97, 'a.', fontsize=24, transform=ax_may.transAxes)
ax_june.text(-0.15, 0.97, 'b.', fontsize=24, transform=ax_june.transAxes)

# save
if FIG_FMT.upper() == 'PDF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig1-python.pdf', dpi=dpi)
elif FIG_FMT.upper() == 'PNG':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig1-python.png', dpi=dpi)
elif FIG_FMT.upper() == 'TIF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig1-python.tif', dpi=dpi)
else:
    print('Unrecognized figure format: "%s" (must be PNG or PDF)' % FIG_FMT)
