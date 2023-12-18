# 1. import libraries
import numpy as np
import pandas as pd
import plotly.express as px # simple graphs
import plotly.graph_objects as go # complex graphs
import streamlit as st

# config
st.set_page_config(layout='wide') # wide layout

# common variables
years = list(range(1980, 2014))

def create_animated_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(rgba(255,255,255,0.5), rgba(100,100,255,0.5)), url("https://images.unsplash.com/photo-1539604214100-ab860d9082e0?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }
       .sidebar .sidebar-content {
            background: url("https://images.unsplash.com/photo-1503437313881-503a9122641a?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FuYWRhJTIwc2FpbnR8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80")
        }
        </style>
        """,
        unsafe_allow_html=True
    )

create_animated_background()

# 2. create function to clean data
def clean_dataset(df):
    df.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True) # drop columns
    df.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region', 'DevName':'Status'}, inplace=True) # rename columns
    df.set_index('Country', inplace=True) # set country as index
    df['Total'] = df[years].sum(axis=1)   # add a total column to the dataframe
    return df

# 3. create function to load data
st.cache()                                # helps to make the app faster
def load_dataset():
    df = pd.read_excel('data/Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=20, skipfooter=2)
    df = clean_dataset(df)
    return df

# 4. setup basic UI
st.title("Immigration from Countries to Canada")
st.subheader("Data from International Organization for Migration (IOM) - United Nations Migration Agency")
with st.spinner("loading dataset"):                          # show a loading message
    df = load_dataset()
    # st.balloons()        
c1,c2 = st.columns(2)                                   # create 2 columns
with c1:
    st.header("Original Data")
    st.dataframe(df, height=350)
with c2:
    st.header("Statistic Summary")
    st.dataframe(df.describe(), height=350)

# 5. give user option to select columns
st.header("Select a country to visualize")
countries = df.index.tolist()
sel_country = st.selectbox("Country", countries)
# graph
st.header(f'trend chart for {sel_country} from {years[0]} to {years[-1]}') 
c1, c2 = st.columns(2)
country = df.loc[sel_country, years] # subset
fig = px.line(country, x=country.index, y=country.values)
c1.plotly_chart(fig, use_container_width=True)
fig = px.box(country, y=country.values)
c2.plotly_chart(fig, use_container_width=True)


st.header("Select multiple countries to visualize")
sel_countries = st.multiselect("Countries", countries)
if len(sel_countries)>1:
    st.header(f'Comparing countries {", ".join(sel_countries)}')
    df_countries = df.loc[sel_countries, years].T # subset
    fig = px.bar(df_countries, x=years, y=sel_countries)
    st.plotly_chart(fig)
else:
    st.warning('Please select at least 2 countries for comparison')
# 6. give user option display graphs

# 0. Run the app run the command below
# streamlit run home.py