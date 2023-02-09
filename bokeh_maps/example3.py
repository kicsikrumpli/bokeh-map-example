import geopandas as gpd
import numpy as np
from bokeh.io import show
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure

# 1. convert shape file to geopandas
shapefile = '../110m_cultural/ne_110m_admin_0_countries.shp'
# Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'LABELRANK', 'geometry']]
# Rename columns.
gdf.columns = ['country', 'country_code', 'label_rank', 'geometry']
gdf['random_color'] = np.random.choice(np.array(['red', 'green', 'blue', 'yellow', 'purple']), size=gdf.shape[0])

height_to_width = 120/198  # from google, mercatorial projection
width = 1000
height = int(width * height_to_width)

geosource = GeoJSONDataSource(geojson=gdf.to_json())
p = figure(title="title",
           #width=width,
           #height=height
           )

p.patches('xs',
          'ys',
          source=geosource,
          # fill_color={
          #     'field': 'label_rank',
          #     'transform': LinearColorMapper(
          #         palette='Viridis256',
          #         low=gdf['lr'].min(),
          #         high=gdf['lr'].max())
          # },
          fill_color={
              'field': 'random_color'
          },
          line_color='black',
          line_width=0.25,
          fill_alpha=1)
show(p)
