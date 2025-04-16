import streamlit as st
from read_data import read_from_gsheets
import altair as alt
from datetime import datetime, timedelta
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="Geometry Summary Statistics - Latest Release",
    layout="wide"
)
filter_list = ["US", "Excluding US", "Grand Total"]
latest_release_df = (
    read_from_gsheets("Global Places")
    [["Country", "Total POI with Parking Lots", "POI with polygons with Parking Lots", "Point-only POI", "Polygon coverage"]]
    .tail(8)
    .query('Country  == @filter_list')
    .assign(
        **{
            "Total POI with Parking Lots": lambda df: df["Total POI with Parking Lots"].str.replace(",", "").astype(float),
            "POI with polygons incl. Parking Lots": lambda df: df["POI with polygons with Parking Lots"].str.replace(",", "").astype(int),
            "Point-only POI": lambda df: df["Point-only POI"].str.replace(",", "").astype(int),
            "Polygon coverage": lambda df: ((df["Polygon coverage"].str.replace(",", "").astype(float)) * 100).astype(float)
        }
    )
    .drop(['POI with polygons with Parking Lots'], axis=1)
    .reset_index(drop=True)
)

column_order = [
    "Country",
    "Total POI with Parking Lots",
    "POI with polygons incl. Parking Lots",
    "Point-only POI",
    "Polygon coverage"
]

latest_release_df = latest_release_df[column_order]
latest_release_df.loc[latest_release_df.Country == "Excluding US", 'Country'] = 'Rest of World'

latest_release_df_styled = (
    latest_release_df.style
    .apply(lambda x: ['background-color: #D7E8ED' if i%2==0 else '' for i in range(len(x))], axis=0)
    .format({
        "Total POI with Parking Lots": "{:,.0f}",
        "POI with polygons incl. Parking Lots": "{:,.0f}",
        "Point-only POI": "{:,.0f}",
        "Polygon coverage": "{:.01f}%"
    })
)

total_poi = latest_release_df.iloc[-1]["Total POI with Parking Lots"]


st.write(f"POI count across all countries, including parking lots POI is <b>{total_poi:,.0f}</b>", unsafe_allow_html=True)
st.dataframe(latest_release_df_styled, use_container_width=True, hide_index=True)


#### Top 30 Geometry ####
top_30_geometry_df = (
    read_from_gsheets("Countries")
    .assign(**{
        "Total POI with Parking Lots": lambda df: df["Total POI with Parking Lots"].astype(int),
        "POI with polygons": lambda df: df["POI with polygons"].str.replace(",", "").astype(int),
        "Point-only POI": lambda df: df["Point-only POI"].str.replace(",", "").astype(int),
        "Polygon coverage": lambda df: ((df["Polygon coverage"].str.replace(",", "").astype(float)) * 100).astype(float)
    })
    .query('iso_country_code != "US"')
    .drop('Total POI', axis=1)
    .rename(columns={"iso_country_code": "Country Code", "country": "Country", "Total POI with Parking Lots":"Total POI"})
    [["Country Code", "Country", "Total POI", "POI with polygons", "Point-only POI", "Polygon coverage"]]
    .head(30)
)

top_30_df_geometry_styled = (
    top_30_geometry_df.style
    .apply(lambda x: ['background-color: #D7E8ED' if i%2==0 else '' for i in range(len(x))], axis=0)
    .format({
       "Total POI": "{:,.0f}",
        "POI with polygons": "{:,.0f}",
        "Point-only POI": "{:,.0f}",
        "Polygon coverage": "{:.01f}%"
    })
)

st.write("POI Counts - Top 30 Countries Outside the US")
st.dataframe(top_30_df_geometry_styled, use_container_width=True, hide_index=True)

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

css = '''
<style>
section.main > div:has(~ footer ) {
     padding-top: 0px;
    padding-bottom: 0px;
}

[data-testid="ScrollToBottomContainer"] {
    overflow: hidden;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Keep-alive comment: 2025-03-29 14:26:57.302101
# Keep-alive comment: 2025-03-31 15:59:01.370751
# Keep-alive comment: 2025-03-31 19:24:40.167499
# Keep-alive comment: 2025-04-01 06:22:21.233923
# Keep-alive comment: 2025-04-01 17:23:14.753482
# Keep-alive comment: 2025-04-02 04:23:00.781456
# Keep-alive comment: 2025-04-02 15:22:59.883706
# Keep-alive comment: 2025-04-03 02:22:34.821758
# Keep-alive comment: 2025-04-03 13:23:39.807063
# Keep-alive comment: 2025-04-04 00:24:02.203456
# Keep-alive comment: 2025-04-04 11:23:33.139493
# Keep-alive comment: 2025-04-04 22:22:44.940590
# Keep-alive comment: 2025-04-05 09:22:35.320006
# Keep-alive comment: 2025-04-05 20:23:50.801180
# Keep-alive comment: 2025-04-06 07:23:20.376829
# Keep-alive comment: 2025-04-06 18:22:52.024159
# Keep-alive comment: 2025-04-07 05:23:15.633866
# Keep-alive comment: 2025-04-07 16:24:14.367437
# Keep-alive comment: 2025-04-08 03:23:30.720614
# Keep-alive comment: 2025-04-08 14:23:46.030129
# Keep-alive comment: 2025-04-09 01:23:14.526261
# Keep-alive comment: 2025-04-09 12:22:55.743524
# Keep-alive comment: 2025-04-09 23:23:15.203781
# Keep-alive comment: 2025-04-10 10:22:23.470332
# Keep-alive comment: 2025-04-10 21:22:48.494972
# Keep-alive comment: 2025-04-11 08:24:59.283258
# Keep-alive comment: 2025-04-11 19:25:20.044961
# Keep-alive comment: 2025-04-12 06:22:56.024155
# Keep-alive comment: 2025-04-12 17:23:09.159221
# Keep-alive comment: 2025-04-13 04:22:25.269239
# Keep-alive comment: 2025-04-13 15:23:23.698102
# Keep-alive comment: 2025-04-14 02:23:44.878899
# Keep-alive comment: 2025-04-14 13:23:08.132480
# Keep-alive comment: 2025-04-15 00:22:53.876570
# Keep-alive comment: 2025-04-15 11:23:15.125279
# Keep-alive comment: 2025-04-15 22:22:59.146863
# Keep-alive comment: 2025-04-16 09:23:38.414326
# Keep-alive comment: 2025-04-16 20:23:28.629740