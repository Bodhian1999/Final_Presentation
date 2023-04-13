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

#api = KaggleApi()
#api.authenticate()

#!kaggle datasets download -d ramjasmaurya/us-police-shootings-from-20152022

#with zipfile.ZipFile("us-police-shootings-from-20152022.zip","r") as zip_ref:
#    zip_ref.extractall()

df = pd.read_csv("US Police shootings in from 2015-22.csv")
df2 = pd.read_csv('Unemployment in America Per US State.csv')

#DATA CLEANING:
df.dropna(how = 'all')
df.dropna(subset=['longitude'], how='all', inplace=True)
df.dropna(subset=['age'], how='all', inplace=True)
df = df.fillna('Unknown')
df2['Total Unemployment in State/Area'] = df2['Total Unemployment in State/Area'].str.replace(',', '').astype(int)
df.dropna(subset=['gender'], how='all', inplace=True)
df['gender'] = df['gender'].str.replace('M','Male')
df['gender'] = df['gender'].str.replace('F','Female')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

####################################
st.header('US Police shootings from 2015-2022 & Unemployment in America')
st.markdown('Bodhian Hardeman & Rojhat Yildirim')

HeaderImage = Image.open('police.jpg')
st.image(HeaderImage, width=700)

st.markdown('**👮‍♂️🔫US Police Shootings from 2015- Sep 2022**')
st.markdown('Doden door politieagenten van 2015 t/m 2022 september volgens **The Counted**')
st.write(df.head())
st.markdown('Aantal rijen en kolommen:')
st.write(df.shape)
st.markdown('.describe():')
st.write(df.describe())

st.markdown('**Unemployment in America, Per US State**')
st.markdown('Arbeidssituatie van Amerikaanse bevolking van January 1976 tot December 2022 volgens **U.S. Bureau of Labor statistics**')
st.write(df.head())
st.write(df.shape)
st.markdown('.describe():')
st.write(df.describe())


#st.markdown('<div style="text-align: right;">(Bron: The Economist)</div>', unsafe_allow_html=True)


