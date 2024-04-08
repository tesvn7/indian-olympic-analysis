import streamlit as st
import pandas as pd
import preprocessor, helpers

# load data
df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

# preprocess data
df = preprocessor.preprocess(df, region_df)

# Set the page configuration to use the wide view
st.set_page_config(layout="wide")

# create sidebar
st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'select an option', 
    ('Medal Tally', 'Overall Analysis', 'Country-wise-Analysis', 'Athlete-wise-Analysis'),
    )

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helpers.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helpers.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

