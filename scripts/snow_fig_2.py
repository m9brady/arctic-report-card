from pathlib import Path

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#### FLAG TO ASSIGN OUTPUT FIGURE FORMAT
FIG_FMT = 'PDF' # or 'PNG' or 'TIF'

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.family'] = 'Arial'

fig_crs = ccrs.LambertAzimuthalEqualArea(central_latitude=90, central_longitude=-80)
data_crs = ccrs.PlateCarree()
figsize = (15, 6.85)
dpi = 100
extent = [-6e6, 5e6, -5e6, 5e6]
cbar_ticks = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]
# copied the RGB values from Arc18_Snow_Fig2.png
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    name='fig2',
    colors=[
        (x[0]/255, x[1]/255, x[2]/255) for x in [
            (255,  47,  34), (255, 113,  57), (239, 162,   0),
            (255, 211,  66), (255, 255, 156), (255, 255, 255),
            (255, 255, 255), (255, 255, 255), (198, 255, 222),
            (140, 211, 255), ( 57, 195, 255), (  0, 150, 189),
            (  0,  95, 206)
        ]
    ],
    N=256
)

data_root = Path(__file__).parent.parent / 'data'
# load netcdf data (snow cover duration, orig type = timedelta)
with xr.open_dataset(data_root / 'ARC_SCD_anomaly_a.nc') as ds:
    data_a = ds['scd'].astype(float)
with xr.open_dataset(data_root / 'ARC_SCD_anomaly_b.nc') as ds:
    data_b = ds['scd'].astype(float)

# make the dummy data more visually-appealing
data_a = 100 * (data_a/data_a.max())
data_b = 100 * (data_b/data_b.max())

# load vector data
land = gpd.read_file(data_root / 'vector' / 'land.gpkg').to_crs(fig_crs.proj4_init)
lakes = gpd.read_file(data_root / 'vector' / 'lakes.gpkg').to_crs(fig_crs.proj4_init)
ac = gpd.read_file(data_root / 'vector' / 'arcticcircle.gpkg').to_crs(fig_crs.proj4_init)
rivers = gpd.read_file(data_root / 'vector' / 'rivers.gpkg').to_crs(fig_crs.proj4_init)

# initialize canvas
fig, (ax_a, ax_b) = plt.subplots(
    figsize=figsize,
    nrows=1,
    ncols=2,
    subplot_kw={'projection': fig_crs}
)

# setting margins
plt.subplots_adjust(top=0.999, bottom=0.001, left=0.001, right=0.999, wspace=0, hspace=0)

# plotting netcdf data
'''
mesh_a = data_a.plot.pcolormesh(
    ax=ax_a, add_colorbar=False, center=0, transform=data_crs, 
    cmap=cmap, vmin=-50, vmax=50
)

mesh_b = data_b.plot.pcolormesh(
    ax=ax_b, add_colorbar=False, center=0, transform=data_crs, 
    cmap=cmap, vmin=-50, vmax=50,
)
'''
# Got the contours to look okay!
contour_a = data_a.plot.contourf(
    ax=ax_a, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks
)
contour_b = data_b.plot.contourf(
    ax=ax_b, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks
)

# setting figure extents
ax_a.set_extent(extent, crs=fig_crs)
ax_a.outline_patch.set_linewidth(1)
ax_b.set_extent(extent, crs=fig_crs)
ax_b.outline_patch.set_linewidth(1)

# adding vector data to map
ax_a.add_geometries(land['geometry'], facecolor='None', edgecolor='black', linewidth=0.4, crs=fig_crs)
ax_b.add_geometries(land['geometry'], facecolor='None', edgecolor='black', linewidth=0.4, crs=fig_crs)

ax_a.add_geometries(lakes['geometry'], facecolor='white', edgecolor='black', linewidth=0.4, zorder=2, crs=fig_crs)
ax_b.add_geometries(lakes['geometry'], facecolor='white', edgecolor='black', linewidth=0.4, zorder=2, crs=fig_crs)

ax_a.add_geometries(ac['geometry'], facecolor='None', edgecolor='black', linestyle='dashed', linewidth=1.5, alpha=0.4, zorder=3, crs=fig_crs)
ax_b.add_geometries(ac['geometry'], facecolor='None', edgecolor='black', linestyle='dashed', linewidth=1.5, alpha=0.4, zorder=3, crs=fig_crs)

ax_a.add_geometries(rivers['geometry'], facecolor='None', edgecolor='black', linewidth=0.3, crs=fig_crs)
ax_b.add_geometries(rivers['geometry'], facecolor='None', edgecolor='black', linewidth=0.3, crs=fig_crs)

# adding colorbars
caxa = inset_axes(ax_a, width='5%', height='55%', loc=3, bbox_to_anchor=(0.015, 0.015, 1, 1), bbox_transform=ax_a.transAxes)
cb_a = plt.colorbar(contour_a, cax=caxa, ticks=cbar_ticks, orientation='vertical')
ax_a.text(0.015, 0.61, 'days', fontsize=18, transform=ax_a.transAxes)
cb_a.ax.tick_params(labelsize=14)

caxb = inset_axes(ax_b, width='5%', height='55%', loc=3, bbox_to_anchor=(0.015, 0.015, 1, 1), bbox_transform=ax_b.transAxes)
cb_b = plt.colorbar(contour_b, cax=caxb, ticks=cbar_ticks, orientation='vertical')
ax_b.text(0.015, 0.61, 'days', fontsize=18, transform=ax_b.transAxes)
cb_b.ax.tick_params(labelsize=14)

# axis text indicators
ax_a.text(0.02, 0.94, 'a.', fontsize=30, transform=ax_a.transAxes)
ax_b.text(0.02, 0.94, 'b.', fontsize=30, transform=ax_b.transAxes)

# save
if FIG_FMT.upper() == 'PDF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig2-python.pdf', dpi=dpi)
elif FIG_FMT.upper() == 'PNG':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig2-python.png', dpi=dpi)
elif FIG_FMT.upper() == 'TIF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig2-python.tif', dpi=dpi)
else:
    print('Unrecognized figure format: "%s" (must be PNG or PDF)' % FIG_FMT)
