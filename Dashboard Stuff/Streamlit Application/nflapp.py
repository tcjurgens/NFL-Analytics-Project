# from types import NoneType

import pandas as pd
# from pandas.core import indexing
# from pandas.core.indexes.base import Index
# from pandas.core.indexes.numeric import NumericIndex  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import base64
from PIL import Image
import numpy as np
import csv

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# emojis2: https://slackmojis.com/categories/5-nfl-emojis
st.set_page_config(page_title="NFL Analytics", page_icon=":football:", layout="wide")

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

side_bar = """
  <style>
    /* The whole sidebar */
    .css-vqjv8de1fqkh3o1{
      margin-top: 3rem;
    }
     
     /* The display arrow */
    .css-sg054d.e1fqkh3o3 {
      font-size:24px;
      margin-top: 30px;
      }
    
    .css-145z983.effi0qh0{
    font-size: 24px;}

  </style> 
  """
st.markdown(side_bar, unsafe_allow_html=True)

# get excel 
@st.cache
# def get_data_from_excel():
#     df = pd.read_excel(
#     	io='nfl_dashboard_v2.xlsx',
#     	engine='openpyxl',
#     	sheet_name='NFL',
#     	skiprows=3,
#     	usecols='B:H',
#     	nrows=150,
#     )
#     # make the season just the year
#     # df["Season"] = pd.DatetimeIndex(df["Season"]).year
#     df.index = [""] * len(df)
#     df.sort_values(by=['away_team'], ascending=False)
#     # df['predicted_winner'] = df['predicted_winner'].astype(str)
    
#     return df

# df = get_data_from_excel()

# df['predicted_winner'] = df['predicted_winner'].astype(str)
def get_data():
    df = pd.read_csv('nfl_dashboard_v3.csv')
    df.index = [""] * len(df)
    
    return df

df = get_data()

# st.table(df)

# df.index = [""] * len(df)
# st.table(df)
# print(df.to_string(index=False))


# df['home_team'] = df.groupby('home_team')['home_team'].transform(pd.Series.value_counts)
# df.drop(['home_team'], axis = 0, inplace = True)

# st.dataframe(df)

# side panel
st.sidebar.header("Please Filter Here:")
# hometeams = pd.DataFrame({'labels':["ARI"]})
# homeTeamSelect = st.multiselect(
    # "What are your favorite colors",
    # options=list(names['labels']), # convert to list
    # default=["ARI"]
# )


hometeamlist = st.sidebar.selectbox("Select Home Team", df["home_team"].unique())
awayteamlist = st.sidebar.selectbox("Select Away Team", df["away_team"].unique())
weeklist = st.sidebar.selectbox("Select Week of Season", df["season_week"].unique())



# HomeTeam = st.sidebar.multiselect(
    # "Select the Home Team:",
    # options=df["home_team"],
    # default=['TB'],
# )
# 
# AwayTeam = st.sidebar.multiselect(
    # "Select the Away Team:",
    # options=df["away_team"],
    # default=['DAL'],
# )

# SeasonWeek = st.sidebar.multiselect(
    # "Select the Week:",
    # options=df["season_week"].unique(),
    # default=df['1'],
# )

# Starting_QB = st.sidebar.multiselect(
    # "Select the Starting QB:",
    # options=df["Starting_QB"].unique(),
    # default=df["Starting_QB"].unique()
# )

df_selection = df.query(
    "home_team == @hometeamlist & away_team ==@awayteamlist & season_week == @weeklist"
    #  & week == @SeasonWeek"
)

# st.dataframe(df_selection)
# st.dataframe(df_selection.assign(fuck='').set_index('fuck'))


# main page
main_title = '<p style="font-family:fantasy; color:White; font-size: 50px;">NFL Analytics Project</u></p>'
st.markdown(main_title, unsafe_allow_html=True)
# st.markdown("Moist")

# summary row
try:
    PredictedWinner = df_selection["predicted_winner"].iloc[0]
except ValueError:
    st.error('Please choose a valid matchup')


# PredictedWinner2 = PredictedWinner.tolist()
# PredictedWinner3 = PredictedWinner2.get(object, default=None)
try:
    ActualWinner = df_selection["actual_winner"].iloc[0]
except ValueError:
    st.error('Please choose a valid matchup')
try:
    WinProbability = df_selection["win_probability"].iloc[0]
except ValueError:
    st.error('Please choose a valid matchup')

# star_rating = ":football:" * (WinProbability, 0)
# average_spread_result = round(df_selection["Spread_Result"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    predicted_title = '<p style="font-family:sans-serif; color:White; font-size: 32px;"><u>Predicted Winner:</u></p>'
    st.markdown(predicted_title, unsafe_allow_html=True)
    # st.subheader({PredictedWinner}, anchor=None)
    st.subheader(f"{PredictedWinner}")
with middle_column:
    winner_title = '<p style="font-family:sans-serif; color:White; font-size: 32px;"><u>Actual Winner:</u></p>'
    st.markdown(winner_title, unsafe_allow_html=True)
    # st.subheader("Actual Winner:")
    # st.subheader({ActualWinner}, anchor=None)
    st.subheader(f"{ActualWinner}")
with right_column:
    model_title = '<p style="font-family:sans-serif; color:White; font-size: 32px;"><u>Model Confidence:</u></p>'
    # st.subheader("Model Confidence:")
    st.markdown(model_title, unsafe_allow_html=True)
    # st.markdown("Using our ML model, this was the accuracy of prediction")
    # st.subheader({WinProbability}, anchor=None)
    st.subheader(f"{WinProbability}")
    
   
# 
st.markdown("""---""")


nfl_sched = Image.open('nfl-schedule-2021.png')
nfl_schedule = '<p style="font-family:sans-serif; color:White; font-size: 32px;"><u>2021 NFL Schedule:</u></p>'
st.markdown(nfl_schedule, unsafe_allow_html=True)

st.image(nfl_sched)  
   
# 
st.markdown("""---""")
# 
# Points by team bar chart
# points_by_team = (
    # df_selection.groupby(by=["Team"]).sum()[["Points_Scored"]].sort_values(by="Points_Scored")
# )
# fig_team_points = px.bar(
    # points_by_team,
    # x="Points_Scored",
    # y=points_by_team.index,
    # orientation="h",
    # title="<b>Points by Team</b>",
    # color_discrete_sequence=["#0083B8"] * len(points_by_team),
    # template="plotly_white",
# )
# fig_team_points.update_layout(
    # plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False))
# )
# 
# st.plotly_chart(fig_team_points)

# Bar chart for spread
# points_vs_spread = df_selection.groupby(by=["Team"]).sum()[["Spread_Result"]]
# fig_points_vs_spread = px.bar(
    # points_vs_spread,
    # x=points_vs_spread.index,
    # y="Spread_Result",
    # title="<b>Spread Results</b>",
    # color_discrete_sequence=["#0083B8"] * len(points_vs_spread),
    # template="plotly_white",
# )
# fig_points_vs_spread.update_layout(
    # xaxis=dict(tickmode="linear"),
    # plot_bgcolor="rgba(0,0,0,0)",
    # yaxis=(dict(showgrid=False)),
# )
# 
# 
# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_team_points, use_container_width=True)
# right_column.plotly_chart(fig_points_vs_spread, use_container_width=True)
# 
# 

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
