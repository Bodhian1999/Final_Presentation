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



df = pd.read_csv('US Police shootings in from 2015-22.csv')
df2 = pd.read_csv('Unemployment in America Per US State.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = df.drop(columns=['name'])

df.dropna(subset=['longitude'], how='all', inplace=True)
df.dropna(subset=['age'], how='all', inplace=True)
df.dropna(subset=['gender'], how='all', inplace=True)


df['gender'] = df['gender'].str.replace('M','Male')
df['gender'] = df['gender'].str.replace('F','Female')


df = df.fillna('Unknown')

df['date'] = pd.to_datetime(df['date'])

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

pio.templates.default = "plotly"

fig1 = px.bar(df.groupby(by='year').count().date,
              title='Number of Shootings by year')

fig1.update_layout(title={'text': 'Number of Shootings per Year'},
                  showlegend=False,
                  xaxis_title='Year',
                  yaxis_title='Count')

df_year_month = df.groupby(by=['year','month']).count().date
df_year_month = df_year_month.reset_index().pivot('year','month','date').transpose()

fig2 = px.line(np.cumsum(df_year_month),markers=True)

fig2.update_layout(title={'text': 'Number of Cumulative Shootings per Year'},
                  xaxis_title='Year',
                  yaxis_title='Count',
                  legend_title='Year')

df_year_month = df.groupby(by=['year','month']).count().date
df_year_month = df_year_month.reset_index().pivot('year','month','date').transpose()

fig3 = px.line(df_year_month,markers=True)

fig3.update_layout(title={'text': 'Number of Shootings per Month per Year'},
                  xaxis_title='Year',
                  yaxis_title='Count',
                  legend_title='Year')

fig4 = px.density_heatmap(df, x='year', y='month')

fig4.update_layout(title={'text': 'Number of Shootings per Year and Month'},
                  xaxis_title='Year',
                  yaxis_title='Month',
                  coloraxis_colorbar=dict(title="Occurances"))


df_year_state = df.groupby(by=['year','state']).count().date
df_year_state = df_year_state.reset_index()
df_year_state.columns = ['year','state','count']


df3 = pd.DataFrame(df.groupby(['state','gender','race','flee','armed','threat_level','manner_of_death','signs_of_mental_illness']).size())
df3.reset_index(inplace=True)
df3.rename(columns = {0:'Occurences'}, inplace = True)
df3.head()

fig5 = px.treemap(df3,
                 path=[px.Constant('USA'),'state','gender','race','flee','armed','manner_of_death'],
                 values='Occurences',
                 color='Occurences',
                 color_continuous_scale='YLOrRd')

st.markdown('**Verschillende Grafieken Voor Schietpartijen per Jaar**')

knoppen = ['Number of Shootings per Year','Number of Cumulative Shootings per Year','Number of Shootings per Month per Year','Heatmap Shootings per Year and Month',]

gekozen_knoppen = st.selectbox('**Welke plot wil je zien?**', options = knoppen)

if gekozen_knoppen == 'Number of Shootings per Year':

  st.plotly_chart(fig1)

if gekozen_knoppen == 'Number of Cumulative Shootings per Year':

  st.plotly_chart(fig2)

if gekozen_knoppen == 'Number of Shootings per Month per Year':

  st.plotly_chart(fig3)

if gekozen_knoppen == 'Heatmap Shootings per Year and Month':

  st.plotly_chart(fig4)

st.markdown('**Tree Map**')
st.plotly_chart(fig5)


