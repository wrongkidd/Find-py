# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 11:30:38 2022

@author: kim
"""
import streamlit as st


#-------------config file--------------
def configuration():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.title("GEOLOCATIONAL DATA ANALYSIS USING K MEANS CLUSTERING")

    
    hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

