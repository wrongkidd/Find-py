import streamlit as st
from PIL import Image
st.set_page_config(page_title='Find Py',page_icon=Image.open('C:/Users/user/Documents/PROJECT/geolocation/logo.png'),layout="wide",initial_sidebar_state='collapsed')
#img=Image.open('C:/Users/user/Documents/PROJECT/geolocation/logo.png')

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 11:08:43 2022

@author: kim

"""
#--------GEOLOCATIONAL_DATA_ANALYSIS_USING_K_MEANS_CLUSTERING---------

import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation
import geopandas as gpd
import matplotlib.cm as cm
import folium


from streamlit_folium import folium_static 
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image 
from IPython.core.display import HTML 
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize


import config
import sidebar
print("All packages imported!")


config.configuration()

sidebar.menu()



























