from pathlib import Path

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import xarray as xr

fig_crs = ccrs.LambertAzimuthalEqualArea(central_latitude=90, central_longitude=-80)
data_crs = ccrs.PlateCarree()
figsize = (15,8)
dpi = 100
extent = [-6e6, 5.4e6, -5e6, 5e6]
cmap = mpl.cm.coolwarm
norm = mpl.colors.Normalize(vmin=-50, vmax=50)
cbar_ticks = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]

data_root = Path(__file__).parent.parent / 'data'

# load netcdf data (snow cover duration, orig type = timedelta)
with xr.open_dataset(data_root / 'ARC_SCD_anomaly_a.nc') as ds:
    data_a = ds['scd'].astype(float)
with xr.open_dataset(data_root / 'ARC_SCD_anomaly_b.nc') as ds:
    data_b = ds['scd'].astype(float)

# load vector data
land = gpd.read_file(data_root / 'vector' / 'land.gpkg').to_crs(fig_crs.proj4_init)
#lakes = gpd.read_file(data_root / 'vector' / 'lakes.gpkg').to_crs(fig_crs.proj4_init)
#rivers = gpd.read_file(data_root / 'vector' / 'rivers.gpkg').to_crs(fig_crs.proj4_init)

fig, (ax_a, ax_b) = plt.subplots(
    figsize=figsize,
    nrows=1,
    ncols=2,
    subplot_kw={'projection':fig_crs}
)

# setting margins
plt.subplots_adjust(top=0.99, bottom=0.01, left=0.01, right=0.99, wspace=0, hspace=0)

# plotting netcdf data
mesh_a = data_a.plot(
    ax=ax_a, add_colorbar=False, center=0, transform=data_crs, 
    cmap=cmap, norm=norm
)
mesh_b = data_b.plot(
    ax=ax_b, add_colorbar=False, center=0, transform=data_crs, 
    cmap=cmap, norm=norm
)

# setting figure extents
ax_a.set_extent(extent, crs=fig_crs)
ax_a.outline_patch.set_linewidth(0.5)
ax_b.set_extent(extent, crs=fig_crs)
ax_b.outline_patch.set_linewidth(0.5)

# adding vector data to map
ax_a.add_geometries(land['geometry'], facecolor='None', edgecolor='black', linewidth=0.4, crs=fig_crs)
ax_b.add_geometries(land['geometry'], facecolor='None', edgecolor='black', linewidth=0.4, crs=fig_crs)

#ax_a.add_geometries(lakes['geometry'], facecolor='white', edgecolor='black', linewidth=0.4, crs=fig_crs)
#ax_b.add_geometries(lakes['geometry'], facecolor='white', edgecolor='black', linewidth=0.4, crs=fig_crs)

#ax_a.add_geometries(rivers['geometry'], edgecolor='black', linewidth=0.15, crs=fig_crs)
#ax_b.add_geometries(rivers['geometry'], edgecolor='black', linewidth=0.15, crs=fig_crs)


# adding colorbars
caxa = inset_axes(ax_a, width='5%', height='55%', loc=3)
cb_a = plt.colorbar(mesh_a, cax=caxa, ticks=cbar_ticks, orientation='vertical')
cb_a.solids.set_edgecolor("face")

caxb = inset_axes(ax_b, width='5%', height='55%', loc=3)
cb_b = plt.colorbar(mesh_b, cax=caxb, ticks=cbar_ticks, orientation='vertical')

# axis text indicators
ax_a.text(0.02, 0.94, 'a.', family='Arial', fontweight='bold', fontsize=32, transform=ax_a.transAxes)
ax_b.text(0.02, 0.94, 'b.', family='Arial', fontweight='bold', fontsize=32, transform=ax_b.transAxes)

plt.show()
#plt.savefig(data_root.parent / 'scratch' 'test.png', dpi=300)
