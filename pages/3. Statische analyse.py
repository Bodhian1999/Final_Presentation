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

####################################


df3 = df.groupby(['date']).size().reset_index()
df3 = pd.DataFrame(df3)
df3 = df3.rename(columns={0: 'aantal_doden'})
#datetime van maken
df3['date'] = pd.to_datetime(df3['date'])
#int van maken
df3['aantal_doden'] = pd.to_numeric(df3['aantal_doden'])
#Maanden verlopen
df3['months_since_start'] = (df3['date'].dt.year - df3['date'].dt.year.min()) * 12 + (df3['date'].dt.month - df3['date'].dt.month.min())
#Aantal doden per maand
df3['aantal_doden_maand'] = df3.groupby([df3['date'].dt.year, df3['date'].dt.month])['aantal_doden'].transform('sum')
df3.head()

sns.set(style='darkgrid')
fig, ax = plt.subplots(figsize=(10,10))
sns.regplot(x='months_since_start', y='aantal_doden_maand', data=df3, ax=ax, color='blue', line_kws={'color': 'red'})

ax.set_xlabel('Year', fontsize=16, fontweight='bold')
ax.set_ylabel('Deaths', fontsize=16, fontweight='bold')
ax.set_title('Regression plot deaths each month by US police agents', fontsize=20, fontweight='bold')

ax.xaxis.set_tick_params(labelsize=14)
ax.yaxis.set_tick_params(labelsize=14)

ax.xaxis.set_major_locator(ticker.FixedLocator([0, 12, 24, 36, 48, 60, 72, 84, 96]))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']))

st.pyplot(fig, ax)
