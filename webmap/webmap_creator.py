import folium
import pandas as pd
import math
import numpy as np

def get_percentile(l, p) :
    """
        function that returns the p-th percentile from a list

        :param l    The original list
        :param p    The percentile
        :return     The number at that specific percentile
    """
    cpy = list(l)
    cpy.sort()

    poz = len(cpy) * p
    poz = math.ceil(poz)

    return cpy[poz]

in_file = input("Please specify the file were we collect the data from : ")
out_file = "webmap.html"

#read data from the file
df = pd.read_csv(in_file)

#setting the map center in the mean of LAT and LON
map_center = [
    np.mean(df["LAT"]),
    np.mean(df["LON"])
]

#initiating the map object
map = folium.Map(location= map_center, zoom_start = 6, tiles = 'Stamen Terrain')


#getting the limits for elevation intervals
limit1 = get_percentile(df["ELEV"], .33)
limit2 = get_percentile(df["ELEV"], .66)

#building the coulurs list

colours = [
    'green' if e < limit1 else
    'orange' if e < limit2
    else 'red'
    for e in df["ELEV"]
]

for colour, name, lat, lon in zip(colours, df["NAME"], df["LAT"], df["LON"]):
    #add a marker for every volcano
    map.add_child(folium.Marker(location = [lat, lon], popup=name, icon = folium.Icon(color = colour, icon_color = colour)))

#creating the HTML for the map
map.save(out_file)
