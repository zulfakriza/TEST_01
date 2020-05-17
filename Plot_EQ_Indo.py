import pandas as pd
import pygmt
import rioxarray
import skimage.exposure
import xarray as xr
#-------------
#load EQ data from usgs
quakes = pd.read_csv("https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime=1976-01-01%2000:00:00&endtime=2020-05-17%2023:59:59&maxlatitude=11.711&minlatitude=-18.963&maxlongitude=153.984&minlongitude=86.484&minmagnitude=5&maxmagnitude=9.5&mindepth=0&maxdepth=500&orderby=time", skipinitialspace=True )
print(quakes.head())
#skipinitialspace=True

#creating figure and plot EQ hypocentre
fig = pygmt.Figure()
with pygmt.clib.Session() as session:
    session.call_module('gmtset', 'FONT 12p')
   #session.call_module('gmtset', 'MAP_FRAME_TYPE fancy')
    session.call_module('gmtset', 'MAP_FRAME_TYPE plain')
#plot basemap
fig.basemap(region=[92, 144, -12, 10], projection="M8i", frame = "a")
#fig.basemap(region=[92, 144, -12, 10], projection="M8i", frame = Fancy)
fig.coast(shorelines="0.5p,black", land="gray", water="white")
#plot hypocenter 
#fig.plot(x=quakes.longitude, y=quakes.latitude, style="c0.2c", color="red", pen="black")

#plot hypocenter with magnitude scale
#fig.plot(x=quakes.longitude,y=quakes.latitude,sizes=0.01 * (1.5 ** quakes.mag),style="cc",color="red",pen="black")

#plot hypocenter with magnitude scale and depth gradation color
fig.plot(
    x=quakes.longitude,
    y=quakes.latitude,
    sizes=0.01 * 1.6 ** quakes.mag,
    color=quakes.depth / quakes.depth.max(),
    cmap="roma",
    style="cc",
    pen="black",
)

pygmt.makecpt(cmap="roma", series=[0, 500])
fig.colorbar(frame=["xaf", r"y+l\EQ_Dept(Km)"], position= "g92.0/-16.0+w5c/0.4c+h", scale=1)

#save map
fig.savefig("Indonesia_EQ_USGS.png")
