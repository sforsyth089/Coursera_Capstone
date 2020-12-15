#!/usr/bin/env python
# coding: utf-8

# <b>Coursera Peer Review Assignment
# Assess Best Upscale Restaurant Location in Michigan, USA

#  <b>Use the Notebook to build the data frames </b>

# In[8]:


#Import needed items
import pandas as pd
import requests
import numpy as np
from pandas.io.json import json_normalize  
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import json


# In[9]:


# Load Michigan Zip Code data with latitude/longitude


# Load data - This is available on my GitHub
MIZip_data=pd.read_csv('https://raw.githubusercontent.com/sforsyth089/Coursera_Capstone/main/MI%20Zip%20Codes%20Lat%20Long.csv', index_col=0)
MIZip_data


# In[10]:


#Drop fields that we will not use - timezone and daylight savings flag.

MIZip_data.drop("Timezone", axis=1, inplace=True)
MIZip_data.drop("Daylight savings time flag", axis=1, inplace=True)
MIZip_data

#This is the pure ZIP CODE table with latitide and longitude. Next I'd like to combine with the wealth table.


# In[11]:


# Load Michigan Zip Code WEALTH data, Top 25 neighborhoods


# Load data - This is available on my GitHub
MIWealth_data=pd.read_csv('https://raw.githubusercontent.com/sforsyth089/Coursera_Capstone/main/Wealthiest%20Neighborhoods%20in%20MI.csv', index_col=0)
MIWealth_data


# In[39]:





# <b>Combine the Zip and Wealth data to make a data frame.  Drop anything not on the wealth table. </b>

# In[ ]:





# In[12]:


#merging the tables to make 1 new table
df_MItotalwealth = pd.merge(MIZip_data, MIWealth_data, how='left', left_on = 'Zip', right_on = 'Zipcode')

df_MItotalwealth
#This is the merged table. There is too much stuff need to remove the rows that do not make the wealth list.


# In[13]:


#If the zip code is NaN, a match was not found and we drop.

dfwealthclean = df_MItotalwealth.dropna()

dfwealthclean


# <b> Now we will map the MI places and think about a location! </b>

# Create a Michigan Map
# 
# Involves importing folium which is a mapping tool.

# In[18]:


import folium #mapping tool

#Detroit latitude and longitude 42.3314° N, 83.0458° W

map_locationMI = folium.Map(location=[42.3314,-83.0458],zoom_start=10)  

for lat, lng, zipc, neighborhood in zip(dfwealthclean['Latitude'],dfwealthclean['Longitude'],dfwealthclean['Zipcode'],dfwealthclean['Zip Name']):
    label = '{}, {}'.format(neighborhood, zipc)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='blue',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(map_locationMI)
map_locationMI


# 

# 
# Interesting, we see many more blue dots outside of Detroit, but near to Detroit.  
# There are also a couple blue dots in the Traverse City area.

# Next we will cluster the neighboor hoods to think about where we are seeing patterns.

# In[16]:


from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors
dfwealthclean.head()


# This code below does the K means then inserts cluster to the Toronto Only table.

# In[20]:


k=5
MIwealth_clustering = dfwealthclean.drop(['Zipcode','Zip Name', 'City', 'State', 'geopoint', 'County', 'Adjusted Gross Income', 'Median Household Income'],1)
kmeans = KMeans(n_clusters = k,random_state=0).fit(MIwealth_clustering)
kmeans.labels_
dfwealthclean.insert(0, 'Cluster', kmeans.labels_)


# In[21]:


dfwealthclean


# Success - all the neighborhoods have a Cluster assigned

# Next let's map the clusters. Used Detroit as central point. Zoom in/out of map to see more.

# In[23]:


map_MIclusters = folium.Map(location=[42.3314,-83.0458],zoom_start=10)

#colors for mapping
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# markers for mapping
markers_colors = []
for lat, lon, neighborhood, cluster in zip(dfwealthclean['Latitude'], dfwealthclean['Longitude'], dfwealthclean['Zip Name'], dfwealthclean['Cluster']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_MIclusters)
       
map_MIclusters


# Analysis:
# Detroit is a thought of a location, however, there are many more purple dots in the Oakland county area around Birmingham where there are high wealth zip codes which we know will aid in success of our restaurant.

# In[ ]:




