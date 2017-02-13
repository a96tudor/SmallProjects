"""
    US Webmap with markers based on data from a given CSV file

    MIT Standard Licence -- © Tudor Avram -- 13/02/17
"""
import folium
import pandas as pd
import numpy as np
import simple_stats as stats

def get_colours(e_list) :
    """

    :param e_list:      The list of elevations
    :return:            The colours sequence for the given elevations
    """
    # getting the limits for elevation intervals
    limit1 = stats.get_percentile(e_list, .33)
    limit2 = stats.get_percentile(e_list, .66)

    # building the coulurs list

    colours = [
        'green' if e < limit1 else
        'orange' if e < limit2
        else 'red'
        for e in e_list
        ]

    return colours

def read_input():
    """
        Reads the data required to generate the webmap
    :return:    the path for the input file
    """
    in_file = input("Please specify the file were we collect the data from : ")
    return in_file

def process_data(in_file):
    """
        Processing the data from the input file and creating the map
    :param in_file:     The path to the file where we read the data from
    :return:       (1)  The dataframe containing the data
                   (2)  The folium.Map object representing the map
                   (3)  The colours sequence used for the markers
    """
    # read data from the file
    df = pd.read_csv(in_file)

    # setting the map center in the mean of LAT and LON
    map_center = [
        np.mean(df["LAT"]),
        np.mean(df["LON"])
    ]

    # initiating the map object
    map = folium.Map(location=map_center, zoom_start=6, tiles='Stamen Terrain')

    # getting the colors
    colors = get_colours(df["ELEV"])

    return df, map, colors

def add_makers(map, names, lat, lon, colours):
    """
            The function that adds markers to the map
    :param map:         The folium.Map object to add the markers to
    :param names:       The list of makers names
    :param lat:         The list of latitudes
    :param lon:         The list of longitudes
    :param colours:     The list of colours
    :return:            -
    """
    for colour, name, lat, lon in zip(colours, names, lat, lon):
        # add a marker for every volcano
        map.add_child(
            folium.Marker(
                location=[lat, lon],
                popup=name,
                icon=folium.Icon(
                    color=colour,
                    icon_color="yellow")
            )
        )

def main():
    """
        The main function of the program. Connects all the other functions
    :return: -
    """
    #reading input
    in_file = read_input()
    out_file = "markers-webmap.html"

    #processing data and creating the map
    df, map, colours = process_data(in_file)

    #adding the markers to the map
    add_makers(map=map, names=df["NAME"], lat=df["LAT"], lon=df["LON"], colours=colours)
    # creating the HTML for the map
    map.save(out_file)

main()




