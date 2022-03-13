# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 11:55:14 2022

@author: kim
"""

import streamlit as st
import home

def menu():
    st.sidebar.subheader("MENU")
    
    rad=st.sidebar.radio("___________________________________________",["HOME","SETTINGS","ABOUT"])
    if rad=="HOME":
        st.subheader("Home page")
        home.execute()
        
    if rad == "SETTINGS":
        st.subheader("Settings")
    
    
    if rad =="ABOUT":
        st.subheader("coming soon.................")