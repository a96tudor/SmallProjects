import folium
import pandas as pd

map_center = [45.372, -121.697]
in_file = input("Please specify the file were we collect the data from : ")
out_file = "webmap.html"

#initiating the map object
map = folium.Map(location= map_center, zoom_start = 4, tiles = 'Stamen Terrain')

#read data from the file
df = pd.read_csv(in_file)

for  name, lat, lon in zip(df["NAME"], df["LAT"], df["LON"]):
    #add a marker for every volcano
    map.simple_marker(location = [lat, lon], popup=name, marker_color='red')

#creating the HTML for the map
map.save(out_file)