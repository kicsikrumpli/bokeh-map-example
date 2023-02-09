from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import GeoJSONDataSource


output_file("tile.html")

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-6000000, 6000000), y_range=(-7000000, 7000000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(CARTODBPOSITRON)

show(p)

