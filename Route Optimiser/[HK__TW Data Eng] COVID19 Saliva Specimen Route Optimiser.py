#!/usr/bin/env python
# coding: utf-8

# In[26]:


#########################################################################
# Created by Preston Yu (TW Team)
# 2020-08-20
#########################################################################
# First 1 : Import Google Sheet to Jupyter Notebook
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import numpy as np

    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developers.xxxxxxxxx
google_key_file = 'xxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxx')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('Daily Order Request')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[1])
df = df[2:]
df = df.fillna(0)
df['Pickup Longitude'] = df['Pickup Longitude'].astype(np.float64)
df['Pickup Latitude'] = df['Pickup Latitude'].astype(np.float64)
df = df[(df['Pickup Latitude'] >= 22) & (df['Pickup Latitude'] < 24) & (df['Pickup Longitude'] < 115) & (df['Pickup Longitude'] >= 113)]
df = df.reset_index(drop = True)

time.sleep(15)

#########################################################################
# Second 2 : Use KMeans Algorithm to segment the pickup locations
dff = df.iloc[:,5:7]
dff = dff.reset_index(drop = True)

    # import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
    # segment clusters
kmeans = KMeans(n_clusters=10)  # <--- NOTICE: you can change the cluster count by yourself
kmeans.fit(dff)

    # labels
labels = kmeans.predict(dff)
centroids = kmeans.cluster_centers_

fig = plt.figure(figsize=(5, 5))
colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y',5:'m',6:'c',7:'k',8:'navy',9:'teal',10:'gold',
         11:'dimgray',12:'darkviolet',13:'slategrey',14:'peru',15:'tomato',16:'crimson',17:'darkkhaki',18:'azure',19:'lavender',20:'bisque',
         21:'silver',22:'indianred',23:'olive',24:'slateblue',25:'orchid',26:'olivedrab',27:'lightseagreen',28:'lime',29:'tan',30:'lightcoral'}
colors = list(map(lambda x: colmap[x+1], labels))

plt.scatter(dff['Pickup Latitude'], dff['Pickup Longitude'], color=colors, alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx+1])
plt.xlim(22.1, 22.5)
plt.ylim(113.8, 114.5)

pred_df = pd.DataFrame(data = labels, columns = ['route_num_prediction'])

time.sleep(10)

#########################################################################
# Third 3 : Upload prediction data to Google Sheet

    # Backend Setting : https://console.developers.xxxxxxx
    # Connect to Google Sheet
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
    
    # Configure the connection
scope = ['https://spreadsheets.google.com/feeds']
    
    # Give the path to the Service Account Credential 
credentials = ServiceAccountCredentials.from_json_keyfile_name('xxxxxxxx')
    
    # Authorize Jupyter Notebook
gc = gspread.authorize(credentials)
    
    # The gsheet ID
    # Sheet URL : https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxx4
spreadsheet_key = 'xxxxxxxx'
        
    # Set the sheet name for uploading the dataframe
wks_name = 'Route Num Prediction'
cell_of_start_df = 'A1'
    
    # Upload the dataframe
d2g.upload(pred_df,
            spreadsheet_key,
            wks_name,
            credentials = credentials,
            start_cell = cell_of_start_df,
            clean = True)

#time.sleep(30)


# In[37]:


############################################################################
# Fourth 4 : Draw a map
import folium
from shapely import wkt, geometry
import json
from pprint import pprint
from openrouteservice import geocode
import numpy as np

specimen_addresses = []
api_key = 'xxxxxxxxxxxxx'

from openrouteservice import client, places
clnt = client.Client(key=api_key)

wkt_str = 'Polygon ((22.545585 113.800848, 22.154387 113.800848, 22.154387 114.422949, 22.545585 114.422949, 22.545585 113.800848))'
aoi_geom = wkt.loads(wkt_str)
    # get coords from exterior ring
aoi_coords = list(aoi_geom.exterior.coords) 
aoi_centroid = aoi_geom.centroid

m = folium.Map(tiles='OpenStreetMap',location=(aoi_centroid.y, aoi_centroid.x), zoom_start=7)
folium.vector_layers.Polygon(aoi_coords,
                                color='#ffd699',
                                fill_color='#ffd699',
                                fill_opacity=0.2,
                                weight=3).add_to(m)

aoi_json = geometry.mapping(geometry.shape(aoi_geom))
query = {'request': 'pois',
        'geojson': aoi_json,
        'filter_category_ids': [569],
        'sortby': 'distance'}


    # The scope is always look like this so we did not need to change anything
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Name of our Service Account Key
    # https://console.developers.xxxxxxxxxx
google_key_file = 'xxxxxxxxxx'
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_key_file, scope)
gc = gspread.authorize(credentials)

    # Opening the worksheet by using Worksheet ID
workbook = gc.open_by_key('xxxxxxx')

    # Selecting which sheet to pulling the data
sheet = workbook.worksheet('Daily Order Request')

    # Pulling the data and transform it to the data frame
values = sheet.get_all_values()
df = pd.DataFrame(values[:], columns = values[1])
df = df[2:]
df = df.reset_index(drop = True)
    
    # Deduplicate by slightly change a little on latitude value
    #is_dup = pd.Series(df['Pickup Latitude']).duplicated()
    #df = df.where(~is_dup,df['Pickup Latitude'].astype(np.float64) * 1.0000001, axis = 1)
    
    # Filter the Route Cluster
dfa = df[df['Route Num\nPrediction'] == '9']   # <--- NOTICE: you could change the number by yourself, from 0 - 14, it represents route clusters
dfa = dfa.reset_index(drop = True)
dfa['Pickup Longitude'] = dfa['Pickup Longitude'].astype(np.float64)
dfa['Pickup Latitude'] = dfa['Pickup Latitude'].astype(np.float64)

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
gdf = geopandas.GeoDataFrame(
    dfa, geometry=geopandas.points_from_xy(dfa['Pickup Longitude'], dfa['Pickup Latitude']))

for i in range(0,len(dfa)):
    lon = dfa['Pickup Longitude'][i]
    lat = dfa['Pickup Latitude'][i]
    name = gdf['No.'][i]
    popup = "<strong>{0}</strong><br>Lat: {1:.3f}<br>Long: {2:.3f}".format(name, lat, lon)
    icon = folium.map.Icon(color='lightgray',
                        icon_color='#b5231a',
                        prefix='fa')
    folium.map.Marker([lat, lon], icon=icon, popup=popup).add_to(m)
    specimen_addresses.append(name)

############################################################################    
# Fifth 5 : Calculate the route possibilities
from openrouteservice import distance_matrix
import json

    # select a segment
a = gdf

    # transform coordinates
specimen_coords = a['geometry']
specimen_coords = specimen_coords.to_json()
specimen_coords = json.loads(specimen_coords)
specimen_coords = specimen_coords['features']

spec_coords = []
for i in range(0,len(specimen_coords)):
    spec_coords.append(specimen_coords[i]['geometry']['coordinates'])

    # output JSON    
request = {'locations': spec_coords,
           'profile': 'driving-car',
           'metrics': ['duration']}

    # output route matrix
specimen_matrix = clnt.distance_matrix(**request)
print("Calculated {}x{} routes.".format(len(specimen_matrix['durations']),len(specimen_matrix['durations'][0])))

############################################################################  
# Sixth 6 : Calculate the optimal route 
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def getDistance(from_id, to_id):
    return int(specimen_matrix['durations'][from_id][to_id])

tsp_size = len(specimen_addresses)
num_routes = 1
start = 0 # arbitrary start location
coords_aoi = [(y,x) for x,y in aoi_coords] # swap (x,y) to (y,x)

optimal_coords = []

if tsp_size > 0:
    routing = pywrapcp.RoutingModel(tsp_size, num_routes, start)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Create the distance callback, which takes two arguments (the from and to node indices)
    # and returns the distance between these nodes.
    dist_callback = getDistance
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve, returns a solution if any.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        # Total cost of the 'optimal' solution.
        print("Total duration: " + str(round(assignment.ObjectiveValue(), 3) / 60) + " minutes\n")
        index = routing.Start(start) # Index of the variable for the starting node.
        route = ''
        #while not routing.IsEnd(index):
        for node in range(routing.nodes()):
            optimal_coords.append(spec_coords[routing.IndexToNode(index)])
            route += str(specimen_addresses[routing.IndexToNode(index)]) + ' -> '
            index = assignment.Value(routing.NextVar(index))   
        #route += str(specimen_addresses[routing.IndexToNode(index)])
        #optimal_coords.append(spec_coords[routing.IndexToNode(index)]) # <-- round-trip switch on for optimal route
        print("Route:\n" + route)
        
############################################################################  
# Seventh 7 : Draw the route on the map 
from openrouteservice import directions
import os.path

def style_function(color):
    return lambda feature: dict(color=color,
                              weight=3,
                              opacity=1)


radius_setting = []
for i in range(0,len(spec_coords)):
    radius_setting.append(1500)

print('If there is an error when showing the map, please adjust the radius (meter)')

    # See what a 'random' tour would have been
#spec_coords.append(spec_coords[0])  # <-- round-trip switch on for random route
request = {'coordinates': spec_coords,
           'profile': 'driving-car',
           'geometry': 'true',
           'format_out': 'geojson',
            'radiuses': radius_setting         
          }
random_route = clnt.directions(**request)

folium.features.GeoJson(data=random_route,
                        name='Random Specimen Route Crawl',
                        style_function=style_function('#00aeb1'),
                       overlay=True).add_to(m)

    # And now the optimal route
request['coordinates'] = optimal_coords
optimal_route = clnt.directions(**request)
folium.features.GeoJson(data=optimal_route,
                        name='Optimal Specimen Route Crawl',
                        style_function=style_function('#0088bf'),
                       overlay=True).add_to(m)

m.add_child(folium.map.LayerControl())

print('The map will initially display the North Pole, should zoom out and find the location of HK then zoom in the map')
print('Green Line represents a random route, Blue Line represents a optimal route')
    # Draw Map
m


# In[ ]:


# Eighth 8 : Return to the Fourth 4 Step and change the route cluster number, then re-run the above cell again


# In[ ]:




