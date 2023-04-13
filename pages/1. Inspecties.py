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
df = pd.read_csv("US Police shootings in from 2015-22.csv")
df2 = pd.read_csv('Unemployment in America Per US State.csv')

col1, col2 = st.columns(2)

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
df = df.rename(columns={'index': 'gender'})

gender = pd.DataFrame()
gender['counts'] = pd.DataFrame(df['gender'].value_counts())
gender.reset_index(inplace=True)
gender.head()

mental = pd.DataFrame()
mental['counts'] = pd.DataFrame(df['signs_of_mental_illness'].value_counts())
mental.reset_index(inplace=True)
mental.head()   

weapon = pd.DataFrame()
weapon['counts'] = pd.DataFrame(df['armed'].value_counts())
weapon.reset_index(inplace=True)
weapon.head()

death = pd.DataFrame()
death['counts'] = pd.DataFrame(df['manner_of_death'].value_counts())
death.reset_index(inplace=True)
death.head()

fleeing = pd.DataFrame()
fleeing['counts'] = pd.DataFrame(df['flee'].value_counts())
fleeing.reset_index(inplace=True)
fleeing.head()

####################################


with col1:
    #TOP 10 states
    top_10_states = df['state'].value_counts().head(10)

    state_names = {'CA': 'California', 'TX': 'Texas', 'FL': 'Florida', 'AZ': 'Arizona', 'GA': 'Georgia', 'CO': 'Colorado',
               'OH': 'Ohio', 'NC': 'North Carolina', 'WA': 'Washington', 'OK': 'Oklahoma'}

    fig = px.histogram(df[df['state'].isin(top_10_states.index)],
                   x='state',
                   color='state',
                   text_auto=True,
                   category_orders={'state': top_10_states.index.tolist()})

    #fig.update_xaxes(categoryorder='total descending') 
    fig.update_traces(marker=dict(line=dict(width=0.5)))
    fig.update_layout(title={'text': "Top 10 states with Killings by Law Enforcement"},
                  xaxis_title="Sates",
                  yaxis_title="Total Occurences",
                  legend=dict(
                        font=dict(
                            family='sans-serif',
                            size=12,
                            color='black'
                            ),
                        bgcolor='LightSteelBlue',
                        bordercolor='Black',
                        borderwidth=2,
                        itemsizing='trace',
                        title='States')
    )

    fig.for_each_trace(lambda t: t.update(name=state_names[t.name]))

    st.plotly_chart(fig, use_container_width = True)
    st.markdown('In dit plot is er te zien welke staten het meeste leiden onder burgersdoden door politieagenten')

    knoppen = ['Gender', 'Sign of Mental Illness', 'Weapon', 'Manner of Death', 'Fleeing']

    gekozen_knoppen = st.selectbox('**Welke plot wil je zien?**', options = knoppen)

    if gekozen_knoppen == 'Gender':
        fig2 = px.bar(gender,
             x='index',
             y='counts',
             color='index',
             text='counts',
             log_y=True,
             range_y=[1,10000],
             color_discrete_map={'Male':'lightblue','Female':'pink'})
        fig2.update_layout(title={'text': "Victim's Gender"},
                  xaxis_title="Gender",
                  yaxis_title="Total",
                  showlegend=False)
        st.plotly_chart(fig2)

    if gekozen_knoppen == 'Sign of Mental Illness':
        fig3 = px.bar(mental,
             x='index',
             y='counts',
             color='index',
             text='counts',
             log_y=True,
             range_y=[1,10000])

        fig3.update_layout(title={'text': "Sign of Mental Illness"},
                  xaxis_title='Sign of Mental Illness',
                  yaxis_title='Occurences',
                  showlegend=False)

        st.plotly_chart(fig3)

    if gekozen_knoppen == 'Weapon':
        fig4 = px.bar(weapon,
             x='index',
             y='counts',
             color='index',
             log_y=True)

        fig4.update_layout(title={'text': "Types of Weapons",},
                  xaxis_title='Weapon Type',
                  yaxis_title='Occurances',
                  showlegend=False)
        st.plotly_chart(fig4)

    if gekozen_knoppen == 'Manner of Death':
        fig5 = px.bar(death,
             x='index',
             y='counts',
             color='index',
             text='counts',
             log_y=True,
             range_y=[1,10000])

        fig5.update_layout(title={'text': "Manner of Death"},
                  xaxis_title="Manner of Death",
                  yaxis_title="Occurences",
                  showlegend=False)
        st.plotly_chart(fig5)

    if gekozen_knoppen == 'Fleeing':
        fig6 = px.bar(fleeing,
             x='index',
             y='counts',
             color='index',
             text='counts')

        fig6.update_layout(title={'text': "Fleeing"},
                  xaxis_title="Manner of Death",
                  yaxis_title="Occurences",
                  showlegend=False)

        st.plotly_chart(fig6)

with col2:
    #WERKLOOSHEID DOOR DE JAREN
    df4 = df2.groupby(['Year'])['Total Unemployment in State/Area'].apply(lambda x : x.astype(int).sum())
    df4 = pd.DataFrame(df4)
    df4 = pd.DataFrame(df4).reset_index()
    df4 = df4.rename(columns={'Total Unemployment in State/Area': 'Total Unemployment in US approximately'})
    df4 = df4[df4['Year'] > 2014]
    df4['Year'] = pd.to_datetime(df4['Year'].astype(str), format='%Y')
    df4.head()

    st.markdown('**Werkloosheid bevolking VS**')
    fig, ax = plt.subplots()


    # Plot the bar chart
    ax.bar(df4.Year.dt.year, df4['Total Unemployment in US approximately']/1000000)

    # Set the y-axis label
    ax.set_ylabel('Total unemployment in US approximately (millions)')

    # Format the y-axis tick labels to add 2 decimals
    fmt = '{x:,.0f}M'
    tick = ticker.StrMethodFormatter(fmt)
    plt.gca().yaxis.set_major_formatter(tick)

    st.pyplot(fig, ax, use_container_width = True)
    st.markdown('In dit plot is de werkloosheid in de VS door de jaren heen te zien')

    knoppen2 = ["Victim's Age Compared by Gender"]

    gekozen_knoppen2 = st.selectbox('**Welke violin-plot wil je zien?**', options = knoppen2)
    if gekozen_knoppen2 == "Victim's Age Compared by Gender":
        fig7 = px.violin(df, y='age', color='gender', box=True, color_discrete_map={'Male':'lightblue','Female':'pink'})

        fig7.update_layout(title={'text': "Victim's Age Compared by Gender "},
                  xaxis_title="Gender",
                  yaxis_title="Age",
                  height=400,
                  legend_title='Gender')
        st.plotly_chart(fig7)

#DROPDOWN MENU


