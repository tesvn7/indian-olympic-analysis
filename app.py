import streamlit as st
import pandas as pd
import preprocessor, helpers
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

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

if user_menu == 'Overall Analysis':

    st.title("Top :rainbow[Statistics]")

    editions, cities, sports, events, athletes, nations = helpers.top_stats(df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(f':red[{editions}]')
    with col2:
        st.header("Cities")
        st.title(f':red[{cities}]')
    with col3:
        st.header("Sports")
        st.title(f':red[{sports}]')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(f':red[{events}]')
    with col2:
        st.header("Athletes")
        st.title(f':red[{athletes}]')
    with col3:
        st.header("Nations")
        st.title(f':red[{nations}]')

    st.title(':rainbow[Participating Nations] over the years')
    nations_over_time = helpers.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.plotly_chart(fig)
    
    st.title(":rainbow[Events] over the years")
    events_over_time = helpers.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    st.title(":rainbow[Athletes] over the years")
    athlete_over_time = helpers.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.plotly_chart(fig)

    st.title(":rainbow[No. of Events] over the years (Every Sport)")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title("Most :rainbow[successful Athletes]")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helpers.most_successful(df,selected_sport)
    st.table(x)