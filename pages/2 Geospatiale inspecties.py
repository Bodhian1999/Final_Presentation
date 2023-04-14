import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from PIL import Image
import streamlit as st
import numpy as np
import plotly.io as pio
import geopandas as gpd
import plotly.graph_objects as go

st.set_page_config(layout='wide')
col1, col2 = st.columns(2)

df = pd.read_csv("US Police shootings in from 2015-22.csv")
df2 = pd.read_csv('Unemployment in America Per US State.csv')

#DATA CLEANING:
df.dropna(how = 'all')
df.dropna(subset=['longitude'], how='all', inplace=True)
df.dropna(subset=['age'], how='all', inplace=True)
df.dropna(subset=['gender'], how='all', inplace=True)
df = df.fillna('Unknown')
df2['Total Unemployment in State/Area'] = df2['Total Unemployment in State/Area'].str.replace(',', '').astype(int)
df['gender'] = df['gender'].str.replace('M','Male')
df['gender'] = df['gender'].str.replace('F','Female')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

df_year_state = df.groupby(by=['year','state']).count().date
df_year_state = df_year_state.reset_index()
df_year_state.columns = ['year','state','count']

####################################

with col1:
    fig = px.scatter_mapbox(df,
                        lat='latitude',
                        lon='longitude',
                        color='state',
                        hover_name='city',
                        hover_data={'longitude':False,
                                    'latitude':False,
                                    'state':True,
                                    'age':True,
                                    'armed':True,
                                    'flee':True,
                                    'threat_level':True},
                        zoom= 2.7)

    fig.update_layout(mapbox_style='open-street-map', height=550)
    st.plotly_chart(fig, use_container_width=True )

with col2:
    fig2 = px.choropleth(df_year_state,
        locations='state', 
        locationmode="USA-states",
        color='count',
        color_continuous_scale="agsunset", 
        scope="usa",
        animation_frame='year',
        title="Incidents Observed in Each State Over the Year") 
    st.plotly_chart(fig2, use_container_width=True )
