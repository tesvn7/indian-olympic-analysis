import streamlit as st
import pandas as pd
import preprocessor, helpers

# load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# preprocess data
df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'select an option', 
    ('Medal Tally', 'Overall Analysis', 'Country-wise-Analysis', 'Athlete-wise-Analysis'),
    )

if user_menu == 'Medal Tally':
    medal_tally = helpers.medal_tally(df)
    st.table(medal_tally)

