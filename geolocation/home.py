# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:52:20 2022

@author: kim
"""

import streamlit as st
import pandas as pd # library for data analsysis
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
#from pandas.io.json import json_normalize
from pandas import json_normalize
import requests # library to handle requests
import folium
from streamlit_folium import folium_static 
import time

global dfstudents
def execute():
    uploaded_file = st.file_uploader(label="upload dataset as csv or xlsx format", 
                             type=['csv','xlsx'])
    st.warning('uploaded dataset must include the following fields: \n cook, eating_out, employment,ethnic_food, exercise, fruit_day, income, on_off_campus, pay_meal_out, sports,veggies_day')
    
    if uploaded_file is not None:
        print(uploaded_file)
        print("file upload sucessfully")
        try:
            dfstudents=pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            dfstudents=pd.read_excel(uploaded_file)
            
    try:
        def raw_data():
            st.write("successfully uploaded dataset")
            check=st.checkbox("show raw data")
            if check:
                st.dataframe(dfstudents)
      
        def clean_data():
            dfclean=dfstudents[['cook','eating_out','employment','ethnic_food','exercise','fruit_day','income','on_off_campus','pay_meal_out','sports','veggies_day']]
            dfclean.dropna(axis=0,inplace=True)
            check=st.checkbox("show cleaned data")
            if check:
                st.dataframe(dfclean)
                
            #Let us visualise the distrubtion of data         
            #st.bar_chart(dfclean)  
            
            # set number of clusters
            kclusters = 3
            
            # run k-means clustering
            kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(dfclean)
            dfclean['Cluster']=kmeans.labels_
            
            fig, axes = plt.subplots(1,kclusters, figsize=(20, 10), sharey=True)
            axes[0].set_ylabel('Coded Values', fontsize=25)
            
            for k in range(kclusters):
                 plt.sca(axes[k])
                 plt.xticks(rotation=45,ha='right')
                 sns.boxplot(data = dfclean[dfclean['Cluster'] == k].drop('Cluster',1), ax=axes[k])
            #st.pyplot(fig)
            
            st.header("dataset analysis")
            col1, col2 = st.columns([2,1])

            with col1:
                st.subheader("before clustering")
                st.bar_chart(dfclean) 
            
            with col2:
                st.subheader("after clustering")
                st.pyplot(fig)
            
            
            st.subheader('Enter search parameters')
            
            col0, col1, col2, col3 = st.columns(4)
            
            
            with col0:
                search_query = st.selectbox(
                 'search query',
                 ('Hotel', 'Apartment','Hostel') )
            

            with col1:
                radius = st.number_input("Enter the search radius(km)",18000,25000) #Set the radius to 18 kilometres due to traffic constraints 
            
            with col2:
                latitude=st.text_input("latitude")#College location
            
            with col3:
                longitude=st.text_input("longitude")
            
            
            
            CLIENT_ID = '5O2OQN1HOFBER5CQ4VJSEBU3PZ54Z3T31EGTNFJ0V04KSKZI'
            CLIENT_SECRET = 'H2KIZ3QZRGZD2GVCOSSTL04SQ3N0Y5QWEWQKPQ1VTPQNF24R' 
            VERSION = '20180604'
            LIMIT = 200
            
            url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
            
            results = requests.get(url).json()
            # assign relevant part of JSON to venues
            venues = results['response']['venues']
            
            # tranform venues into a dataframe
            dataframe = json_normalize(venues)
            
            check=st.checkbox("show fetched raw data")
            if check:
                st.dataframe(dataframe)
                
                
            #Some categories don't mean much to us, such as ID and referralID. Let's only take the fields relevant to us:
            filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
            dataframe_filtered = dataframe.loc[:, filtered_columns]
            
            # function that extracts the category of the venue
            def get_category_type(row):
                try:
                    categories_list = row['categories']
                except:
                    categories_list = row['venue.categories']
                    
                if len(categories_list) == 0:
                    return None
                else:
                    return categories_list[0]['name']
            
            # filter the category for each row
            dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)
            
            # clean column names by keeping only last term
            dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]
            #dataframe_filtered.drop([4,17,18,21,24,30,43],axis=0,inplace=True) #remove some unwanted locations like hotels
            dataframe_filtered.drop(['cc','country','state','city'],axis=1,inplace=True) #no need for those columns as we know we're in Kerala,IN
            
            check=st.checkbox("show cleaned data from fetch")
            if check:
                st.dataframe(dataframe_filtered) 
            
            #define coordinates of the college
            map_bang=folium.Map(location=[latitude,longitude],zoom_start=12)
            
            # instantiate a feature group for the incidents in the dataframe
            locations = folium.map.FeatureGroup()
            
            latitudes = list(dataframe_filtered.lat)
            longitudes = list( dataframe_filtered.lng)
            labels = list(dataframe_filtered.name)
            
            
            for lat, lng, label in zip(latitudes, longitudes, labels):
                folium.Marker([lat, lng], popup=label,icon=folium.Icon(color='green')).add_to(map_bang)    
                
            # add incidents to map
            map_bang.add_child(locations)
            
            # add incidents to map
            #map_bang.add_child(locations)
            
            check=st.checkbox("map before clustering")
            if check:
                folium_static(map_bang) 
            
            df_evaluate=dataframe_filtered[['lat','lng']]
            
            
            RestList=[]
            latitudes = list(dataframe_filtered.lat)
            longitudes = list( dataframe_filtered.lng)
            for lat, lng in zip(latitudes, longitudes):    
                radius = 5000 #Set the radius to 5 kilometres for convenience
                latitude=lat#Query for the apartment location in question
                longitude=lng
                search_query = 'Restaurant' #Search for any food related locations
                url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
                
                results = requests.get(url).json()
                # assign relevant part of JSON to venues
                venues = results['response']['venues']
                # tranform venues into a dataframe
                dataframe2 = json_normalize(venues)
                filtered_columns = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
                dataframe_filtered2 = dataframe2.loc[:, filtered_columns]
                # filter the category for each row
                dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
                # clean column names by keeping only last term
                dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
                RestList.append(dataframe_filtered2['categories'].count())
                
            df_evaluate['Restaurants']=RestList
            st.dataframe(df_evaluate)
            
            
            FruitList=[]
            latitudes = list(dataframe_filtered.lat)
            longitudes = list( dataframe_filtered.lng)
            for lat, lng in zip(latitudes, longitudes):    
                radius = 5000 #Set the radius to 5 kilometres for convenience
                latitude=lat#Query for the apartment location in question
                longitude=lng
                search_query = 'Market' #Search for any food related locations
                url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
                
                results = requests.get(url).json()
                # assign relevant part of JSON to venues
                venues = results['response']['venues']
                # tranform venues into a dataframe
                dataframe2 = json_normalize(venues)
                filtered_columns = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
                dataframe_filtered2 = dataframe2.loc[:, filtered_columns]
                # filter the category for each row
                dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
                # clean column names by keeping only last term
                dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
                FruitList.append(dataframe_filtered2['categories'].count())
                
            df_evaluate['Fruits,Vegetables,Groceries']=FruitList
            st.dataframe(df_evaluate)
            
            kclusters = 3
            # run k-means clustering
            kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(df_evaluate)
            df_evaluate['Cluster']=kmeans.labels_
            df_evaluate['Cluster']=df_evaluate['Cluster'].apply(str)
            
            
           
            check=st.checkbox("final clustered data")
            if check:
                st.dataframe(df_evaluate) 
                   
                
            #define coordinates of the college
            map_bang=folium.Map(location=[latitude,longitude],zoom_start=12)
            # instantiate a feature group for the incidents in the dataframe
            locations = folium.map.FeatureGroup()
            # set color scheme for the clusters
            def color_producer(cluster):
                if cluster=='0':
                    return 'green'
                elif cluster=='1':
                    return 'orange'
                else:
                    return 'red'
            latitudes = list(df_evaluate.lat)
            longitudes = list(df_evaluate.lng)
            labels = list(df_evaluate.Cluster)
            names=list(dataframe_filtered.name)
            for lat, lng, label,names in zip(latitudes, longitudes, labels,names):
                folium.CircleMarker(
                        [lat,lng],
                        fill=True,
                        fill_opacity=1,
                        popup=folium.Popup(names, max_width = 300),
                        radius=5,
                        color=color_producer(label)
                    ).add_to(map_bang)
            
            # add locations to map
            map_bang.add_child(locations)
            
            folium_static(map_bang)
            
                    
                 
        if uploaded_file is not None:
            #display uploaded data
            raw_data()
            
            #remove unwanted fields from dataset
            clean_data()
            
           
            
        
    except Exception as e:
        print(e)
        
        
        