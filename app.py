import streamlit as st
import pandas as pd
import preprocessor, helpers
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from PIL import Image

# load image assets
img = Image.open('assets/olympics-2.jpeg')

# Set the page configuration to use the wide-view, width
st.set_page_config(page_title= 'Olympics Analysis', page_icon=img, layout="wide", initial_sidebar_state="expanded")

# load data
df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

# preprocess data
df = preprocessor.preprocess(df, region_df)

# create sidebar
st.sidebar.image(img,channels='RGB', use_column_width=True) 
st.sidebar.title(':rainbow[Olympics Analysis]')
st.sidebar.divider()
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
        st.title(":red[#] :rainbow[Overall] Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f':red[#] Medal Tally in :rainbow[{selected_year}] Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f':red[#] :rainbow[{selected_country}] overall performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f':red[#] :rainbow[{selected_country}] performance in :rainbow[{selected_year}] Olympics')
    st.divider()
    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    st.title(":red[#] Top :rainbow[Statistics]")
    st.divider()

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
    st.divider()

    # Line Plot : Nations over time
    st.title(':red[#] :rainbow[Participating Nations] over the years')
    st.divider()
    nations_over_time = helpers.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    
    # Line Plot : Events over time
    st.title(":red[#] :rainbow[Events] over the years")
    st.divider()
    events_over_time = helpers.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # Line Plot : Athletes participation over time
    st.title(":red[#] :rainbow[Athletes] over the years")
    st.divider()
    athlete_over_time = helpers.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # Heatmap : Events of sport over time
    st.title(":red[#] :rainbow[No. of Events] over the years (Every Sport)")
    st.divider()
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    # Table : Top 15 Athletes of a Sport
    st.title(":red[#] Most :rainbow[successful Athletes]")
    st.divider()
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helpers.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise-Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    
    # Line Plot : Year wise Medal Tally
    st.title(f':red[#] {selected_country} :rainbow[Medal Tally] over the years')
    st.divider()
    country_df = helpers.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    # Heatmap : Year wise Medal Tally in every Sport
    st.title(':red[#] ' + selected_country + " :rainbow[excels] in the following sports")
    st.divider()
    pt = helpers.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    # Table : Top 10 Athletes of a country, medal wise
    st.title(":red[#] :rainbow[Top 10 athletes] of " + selected_country)
    st.divider()
    top10_df = helpers.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise-Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Probability distribution plot (pdf): Age vs Medal
    st.title(":red[#] Distribution of :rainbow[Age] wrt :rainbow[Medal]")
    st.divider()
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
    

    # Probability distribution plot : Age wrt Sport (Gold Medalist)
    st.title(":red[#] Distribution of :rainbow[ Age] wrt :rainbow[Sport] (Gold Medalist)")
    st.divider()
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # ScatterPlot : Height vs Weight wrt Medals and Sex
    st.title(':red[#] :rainbow[Height] Vs :rainbow[Weight]')
    st.divider()

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helpers.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(8, 3.5))
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal',style='Sex', size=60)
    st.pyplot(fig, use_container_width=False)
    

    # Line Plot : Men vs Women Participation over the years
    st.title(":red[#] :rainbow[Men] Vs :rainbow[Women] Participation Over the Years")
    st.divider()
    final = helpers.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

