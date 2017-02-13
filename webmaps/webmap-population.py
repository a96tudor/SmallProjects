import folium
import pandas as pd
import numpy as np

def main():
    # defining the colouring function

    limit1 = 10000000
    limit2 = 25000000

    col_func = lambda data: {
        'fillColor': "green" if data['properties']['POP2005'] <= limit1
        else "orange" if data['properties']['POP2005'] <= limit2
        else "red"
    }

    map_center = [0, 0]

    map = folium.Map(location=map_center, zoom_start=3, tiles='MapBoxBright')

    map.add_child(
        folium.GeoJson(
            data=open("world_population.json"),
            name='World population',
            style_function=col_func
        )
    )

    map.save(outfile="population-map.html")

main()



