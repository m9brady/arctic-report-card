from pathlib import Path
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

#### FLAG TO ASSIGN OUTPUT FIGURE FORMAT
FIG_FMT = 'PDF' # or 'PNG' or 'TIF'

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

fig_crs = ccrs.LambertAzimuthalEqualArea(central_latitude=90, central_longitude=-80)
data_crs = ccrs.PlateCarree()
figsize = (11, 10)
dpi = 100
extent = [-5e6, 5e6, -5e6, 5e6]
cbar_ticks = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100]
# copied the RGB values from Arc18_Snow_Fig2.png
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    name='fig3',
    colors=[
        (x[0]/255, x[1]/255, x[2]/255) for x in [
            (188,  15,   1), (255,  70,  53), (255, 142,  67),
            (252, 192,  34), (255, 247, 111), (255, 255, 255),
            (255, 255, 255), (255, 255, 255), (176, 255, 114),
            (152, 246, 227), (104, 187, 255), ( 39, 140, 254),
            (  0,  70, 199), (  9,  16, 158)]
    ],
    N=256
)

data_root = Path(__file__).parent.parent / 'data'
# load netcdf data (snow depth?, orig type = float)
with xr.open_dataset(data_root / 'ARC_SDP_anomaly_a.nc') as ds:
    data_a = ds['sdp']
with xr.open_dataset(data_root / 'ARC_SDP_anomaly_b.nc') as ds:
    data_b = ds['sdp']
with xr.open_dataset(data_root / 'ARC_SDP_anomaly_c.nc') as ds:
    data_c = ds['sdp']
with xr.open_dataset(data_root / 'ARC_SDP_anomaly_d.nc') as ds:
    data_d = ds['sdp']

for data in [data_a, data_b, data_c, data_d]:
    data = data.where(data != 0)

# load vector data
land = gpd.read_file(data_root / 'vector' / 'land.gpkg').to_crs(fig_crs.proj4_init)
lakes = gpd.read_file(data_root / 'vector' / 'lakes.gpkg').to_crs(fig_crs.proj4_init)
ac = gpd.read_file(data_root / 'vector' / 'arcticcircle.gpkg').to_crs(fig_crs.proj4_init)
rivers = gpd.read_file(data_root / 'vector' / 'rivers.gpkg').to_crs(fig_crs.proj4_init)

# initialize canvas
fig, axs = plt.subplots(
    figsize=figsize,
    nrows=2,
    ncols=2,
    sharex=True,
    sharey=True,
    subplot_kw={'projection': fig_crs},
    gridspec_kw={'hspace': 0, 'wspace': 0}
)
((ax_a, ax_b), (ax_c, ax_d)) = axs

# setting margins
plt.subplots_adjust(top=0.999, bottom=0.001, left=0.001, right=0.999)

contour_a = data_a.plot.contourf(
    ax=ax_a, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks, extend='both'
)
contour_b = data_b.plot.contourf(
    ax=ax_b, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks, extend='both'
)
contour_c = data_c.plot.contourf(
    ax=ax_c, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks, extend='both'
)
contour_d = data_d.plot.contourf(
    ax=ax_d, add_colorbar=False, transform=data_crs, 
    cmap=cmap, levels=cbar_ticks, extend='both'
)

# setting figure extents
ax_a.set_extent(extent, crs=fig_crs)
ax_a.outline_patch.set_linewidth(1)
ax_b.outline_patch.set_linewidth(1)
ax_c.outline_patch.set_linewidth(1)
ax_d.outline_patch.set_linewidth(1)

# adding vector data to map
for ax in [ax_a, ax_b, ax_c, ax_d]:
    ax.add_geometries(land['geometry'], facecolor='None', edgecolor='black', linewidth=0.4, crs=fig_crs)
    ax.add_geometries(lakes['geometry'], facecolor='white', edgecolor='black', linewidth=0.4, zorder=2, crs=fig_crs)
    ax.add_geometries(ac['geometry'], facecolor='None', edgecolor='black', linestyle='dashed', linewidth=1.5, alpha=0.4, zorder=3, crs=fig_crs)
    ax.add_geometries(rivers['geometry'], facecolor='None', edgecolor='black', linewidth=0.3, crs=fig_crs)

# colorbar
cb_ax = fig.add_axes([0.92, 0.25, 0.02, 0.5])
cbar = fig.colorbar(contour_a, ax=axs[:, 1], cax=cb_ax, ticks=cbar_ticks, extend='both')

# reset axes positions (pain!)
ax_a.set_position(pos=[0.001, 0.500, 0.45, 0.5])
ax_b.set_position(pos=[0.451, 0.500, 0.45, 0.5])
ax_c.set_position(pos=[0.001, 0.005, 0.45, 0.5])
ax_d.set_position(pos=[0.451, 0.005, 0.45, 0.5])

# axis text indicators
ax_a.text(0.02, 0.94, 'a.', fontsize=24, transform=ax_a.transAxes)
ax_b.text(0.02, 0.94, 'b.', fontsize=24, transform=ax_b.transAxes)
ax_c.text(0.02, 0.94, 'c.', fontsize=24, transform=ax_c.transAxes)
ax_d.text(0.02, 0.94, 'd.', fontsize=24, transform=ax_d.transAxes)

# save
if FIG_FMT.upper() == 'PDF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig3-python.pdf', dpi=dpi)
elif FIG_FMT.upper() == 'PNG':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig3-python.png', dpi=dpi)
elif FIG_FMT.upper() == 'TIF':
    plt.savefig(data_root.parent / 'figures' / 'ARC_Snow_Fig3-python.tif', dpi=dpi)
else:
    print('Unrecognized figure format: "%s" (must be PNG or PDF)' % FIG_FMT)
