## Synopsis

Here are in fact 2 mini-projects, written in Python3 :

(1)  markers webmap -- Generates a map, with markers on it. The markers are set based on a given input through a csv file
<br\>
Note: Currently only working for USA coordinates. Updates to follow
<br\>
(2)  world pupulation webmap -- Generates a world map, with countours for every country and different colours per country, based on
population

## Dependencies

This mini-application is written in python 3.6. For this reason, you will need python 3.6 and a few other libraries to be installed. They are : 
<br \>

(1)[Python 3-6](https://www.python.org/downloads/release/python-360/)
<br \>
(2) [Numpy](http://www.numpy.org/). Can be installed by typing : 

```
pip3 install numpy    
```

(3) Pandas 
```
pip3 install pandas
```
(4) folium 
```
pip3 install folium
```

## Usage

This project is really easy to use. You just have to follow these instructions : 

<br\>

For the makers map code you will need to : 

<br\>

(1) Donwload and unarchive the files <br \>

(2) Run the file markers-webmap.py. If you are running it from a Unix Shell (i.e. Mac OS or Linux), just type this command :  

```bash
python3 markers-webmap.py
```

(3) Specify the file you will be using as your input data (i.e. the file where the markers will be collected from). The file MUST be in a [CSV format](https://en.wikipedia.org/wiki/Comma-separated_value ) and have (at least) the following collumns : 

```
(a) NAME -- A string representing the name of the marker
(b) LAT  -- A floating point number storing the latitude of the marker
(c) LON  -- A floating point number storing the longitude of the marker
(d) ELEV -- An integer representing the elevation of the specific point on the map. This is used to colour 
the markers differently based on elevation.
```

An example of such a CSV file is Volcanoes_USA.txt. 

(4) Once the program finished running, it will generate a [HTML] (https://ro.wikipedia.org/wiki/HyperText_Markup_Language) file that, when opened in the browser, will display the map. 

<br\>

For the population map, it is pretty much the same thing. You only have to run "webmap-population.py" instead of "markers-webma.py". Here you don't have to specify any file, it would just take the data on its own from a json file. The output file in this case will be "population-map.html"


