import json

import geopandas as gpd
import pandas as pd
from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.layouts import column
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, Slider
from bokeh.palettes import brewer
from bokeh.plotting import figure

# source: https://towardsdatascience.com/eda-visualization-in-geopandas-matplotlib-bokeh-9bf93e6469ec

# 1. convert shape file to geopandas
shapefile = '../110m_cultural/ne_110m_admin_0_countries.shp'
# Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
# Rename columns.
gdf.columns = ['country', 'country_code', 'geometry']
gdf.head()

# 2. convert to geojson (bokeh)
df = pd.read_csv('../world_happiness_report/2015.csv')
df_2015 = df[['Country', 'Region', 'Happiness Score']]
merged = gdf.merge(df_2015, left_on='country', right_on='Country', how='left')

# Read data to json
merged_json = json.loads(merged.to_json())

# Convert to str like object
json_data = json.dumps(merged_json)

# 3. Static choropleth map with the Bokeh
geosource = GeoJSONDataSource(geojson=json_data)
palette = brewer['YlGnBu'][7]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette=palette, low=2, high=8)
tick_labels = {'2': 'Index 2', '3': 'Index 3', '4': 'Index 4', '5': 'Index 5', '6': 'Index 6', '7': 'Index 7',
               '8': 'Index 8'}
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=5, width=650, height=30,
                     border_line_color=None, location=(20, 0), orientation='horizontal',
                     major_label_overrides=tick_labels)

# 4. display the bokeh plot
hover = HoverTool(tooltips = [ ('Country/region','@country'),('% Happiness Score', '@Happiness_Score')])


def update_plot(attr, old, new):
    yr = slider.value
    new_data = json_data[yr]
    geosource.geojson = new_data
    p.title.text = 'Happiness Score: %d' % yr


slider = Slider(title = 'Year',start = 2015, end = 2019, step = 1, value = 2015)
slider.on_change('value', update_plot)

p = figure(title='Worldwide happiness score, 2015',
           height=600,
           width=950,
           toolbar_location=None,
           tools=[hover])

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

p.patches('xs',
          'ys',
          source=geosource,
          fill_color={
              'field': 'Happiness_Score',
              'transform': color_mapper
          },
          line_color='black',
          line_width=0.25,
          fill_alpha=1)

p.add_layout(color_bar, 'below')
# output_notebook()

layout = column(p) # , widgetbox(slider))
curdoc().add_root(layout)

output_file("map.html")
show(p)
