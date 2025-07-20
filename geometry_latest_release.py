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
# Keep-alive comment: 2025-04-17 07:22:59.788355
# Keep-alive comment: 2025-04-17 18:25:23.315818
# Keep-alive comment: 2025-04-18 05:22:44.073489
# Keep-alive comment: 2025-04-18 16:22:49.520623
# Keep-alive comment: 2025-04-19 03:23:14.946578
# Keep-alive comment: 2025-04-19 14:22:25.754399
# Keep-alive comment: 2025-04-20 01:22:24.086965
# Keep-alive comment: 2025-04-20 12:23:19.310482
# Keep-alive comment: 2025-04-20 23:22:54.171290
# Keep-alive comment: 2025-04-21 10:23:40.221577
# Keep-alive comment: 2025-04-21 21:23:03.517431
# Keep-alive comment: 2025-04-22 08:23:14.110090
# Keep-alive comment: 2025-04-22 19:23:14.093320
# Keep-alive comment: 2025-04-23 06:22:48.427378
# Keep-alive comment: 2025-04-23 17:22:49.603561
# Keep-alive comment: 2025-04-24 04:22:54.720437
# Keep-alive comment: 2025-04-24 15:23:49.851900
# Keep-alive comment: 2025-04-25 02:22:18.428187
# Keep-alive comment: 2025-04-25 13:23:49.239131
# Keep-alive comment: 2025-04-25 16:08:00.271085
# Keep-alive comment: 2025-04-25 16:17:55.755924
# Keep-alive comment: 2025-04-26 00:23:29.585525
# Keep-alive comment: 2025-04-26 11:23:25.497473
# Keep-alive comment: 2025-04-26 22:22:24.429573
# Keep-alive comment: 2025-04-27 09:22:55.117333
# Keep-alive comment: 2025-04-27 20:22:49.530039
# Keep-alive comment: 2025-04-28 07:23:00.766229
# Keep-alive comment: 2025-04-28 18:23:39.783530
# Keep-alive comment: 2025-04-29 05:23:09.787969
# Keep-alive comment: 2025-04-29 16:23:53.277227
# Keep-alive comment: 2025-04-30 03:22:44.785035
# Keep-alive comment: 2025-04-30 14:22:53.826311
# Keep-alive comment: 2025-05-01 01:23:23.972326
# Keep-alive comment: 2025-05-01 12:22:54.508936
# Keep-alive comment: 2025-05-01 23:22:28.035542
# Keep-alive comment: 2025-05-02 10:23:13.615086
# Keep-alive comment: 2025-05-02 21:22:23.778767
# Keep-alive comment: 2025-05-03 08:22:48.714298
# Keep-alive comment: 2025-05-03 19:23:08.560971
# Keep-alive comment: 2025-05-04 06:23:13.606201
# Keep-alive comment: 2025-05-04 17:22:23.235210
# Keep-alive comment: 2025-05-05 04:23:33.189078
# Keep-alive comment: 2025-05-05 15:22:48.474834
# Keep-alive comment: 2025-05-06 02:23:43.395034
# Keep-alive comment: 2025-05-06 13:22:43.689311
# Keep-alive comment: 2025-05-07 00:22:44.062629
# Keep-alive comment: 2025-05-07 11:22:43.783647
# Keep-alive comment: 2025-05-07 22:22:53.666168
# Keep-alive comment: 2025-05-08 09:22:43.677363
# Keep-alive comment: 2025-05-08 20:22:43.546618
# Keep-alive comment: 2025-05-09 07:22:53.842592
# Keep-alive comment: 2025-05-09 18:23:13.544303
# Keep-alive comment: 2025-05-10 05:22:53.906762
# Keep-alive comment: 2025-05-10 16:22:48.120748
# Keep-alive comment: 2025-05-11 03:22:48.451139
# Keep-alive comment: 2025-05-11 14:22:40.029315
# Keep-alive comment: 2025-05-12 01:22:45.464573
# Keep-alive comment: 2025-05-12 12:23:14.256073
# Keep-alive comment: 2025-05-12 23:22:48.621223
# Keep-alive comment: 2025-05-13 10:23:43.277382
# Keep-alive comment: 2025-05-13 21:22:48.549518
# Keep-alive comment: 2025-05-14 08:22:53.610068
# Keep-alive comment: 2025-05-14 19:23:13.961068
# Keep-alive comment: 2025-05-15 06:23:14.327333
# Keep-alive comment: 2025-05-15 17:23:38.582906
# Keep-alive comment: 2025-05-16 04:23:00.560629
# Keep-alive comment: 2025-05-16 15:21:59.418851
# Keep-alive comment: 2025-05-17 02:22:18.839724
# Keep-alive comment: 2025-05-17 13:22:55.604945
# Keep-alive comment: 2025-05-18 00:22:20.003050
# Keep-alive comment: 2025-05-18 11:22:48.821386
# Keep-alive comment: 2025-05-18 22:22:46.246279
# Keep-alive comment: 2025-05-19 09:23:16.630317
# Keep-alive comment: 2025-05-19 20:22:18.895358
# Keep-alive comment: 2025-05-20 07:22:35.991712
# Keep-alive comment: 2025-05-20 18:23:49.095580
# Keep-alive comment: 2025-05-21 05:22:21.195930
# Keep-alive comment: 2025-05-21 16:22:28.992427
# Keep-alive comment: 2025-05-22 03:22:23.644164
# Keep-alive comment: 2025-05-22 14:22:19.382192
# Keep-alive comment: 2025-05-23 01:22:26.000555
# Keep-alive comment: 2025-05-23 12:22:25.697315
# Keep-alive comment: 2025-05-23 23:22:31.085334
# Keep-alive comment: 2025-05-24 10:22:29.198460
# Keep-alive comment: 2025-05-24 21:22:25.526926
# Keep-alive comment: 2025-05-25 08:22:24.996536
# Keep-alive comment: 2025-05-25 19:22:30.748100
# Keep-alive comment: 2025-05-26 06:22:15.116560
# Keep-alive comment: 2025-05-26 17:22:20.193119
# Keep-alive comment: 2025-05-27 04:22:26.234299
# Keep-alive comment: 2025-05-27 15:22:29.415019
# Keep-alive comment: 2025-05-28 02:22:40.116916
# Keep-alive comment: 2025-05-28 13:22:26.728770
# Keep-alive comment: 2025-05-29 00:22:24.331437
# Keep-alive comment: 2025-05-29 11:22:18.877402
# Keep-alive comment: 2025-05-29 22:22:33.668578
# Keep-alive comment: 2025-05-30 09:22:18.310036
# Keep-alive comment: 2025-05-30 20:22:19.023525
# Keep-alive comment: 2025-05-31 07:22:31.174881
# Keep-alive comment: 2025-05-31 18:22:26.489287
# Keep-alive comment: 2025-06-01 05:22:25.413889
# Keep-alive comment: 2025-06-01 16:22:39.095391
# Keep-alive comment: 2025-06-02 03:22:40.115779
# Keep-alive comment: 2025-06-02 14:22:29.443701
# Keep-alive comment: 2025-06-03 01:22:20.958863
# Keep-alive comment: 2025-06-03 12:22:34.308108
# Keep-alive comment: 2025-06-03 23:22:28.744375
# Keep-alive comment: 2025-06-04 10:22:29.948741
# Keep-alive comment: 2025-06-04 21:22:08.435747
# Keep-alive comment: 2025-06-05 08:22:31.553458
# Keep-alive comment: 2025-06-05 19:22:20.241634
# Keep-alive comment: 2025-06-06 06:22:20.990907
# Keep-alive comment: 2025-06-06 17:22:03.792096
# Keep-alive comment: 2025-06-07 04:22:05.096326
# Keep-alive comment: 2025-06-07 15:22:15.345355
# Keep-alive comment: 2025-06-08 02:22:20.799046
# Keep-alive comment: 2025-06-08 13:22:22.304958
# Keep-alive comment: 2025-06-09 00:22:04.886919
# Keep-alive comment: 2025-06-09 11:22:18.985540
# Keep-alive comment: 2025-06-09 22:22:26.972493
# Keep-alive comment: 2025-06-10 09:22:29.060402
# Keep-alive comment: 2025-06-10 20:22:23.750671
# Keep-alive comment: 2025-06-11 07:22:24.618285
# Keep-alive comment: 2025-06-11 18:24:09.817359
# Keep-alive comment: 2025-06-12 05:22:21.820436
# Keep-alive comment: 2025-06-12 16:22:24.471528
# Keep-alive comment: 2025-06-13 03:22:26.119099
# Keep-alive comment: 2025-06-13 14:22:14.581314
# Keep-alive comment: 2025-06-14 01:22:35.186814
# Keep-alive comment: 2025-06-14 12:22:22.588833
# Keep-alive comment: 2025-06-14 23:22:13.831178
# Keep-alive comment: 2025-06-15 10:21:59.420067
# Keep-alive comment: 2025-06-15 21:22:35.008030
# Keep-alive comment: 2025-06-16 08:22:30.215416
# Keep-alive comment: 2025-06-16 19:22:14.714066
# Keep-alive comment: 2025-06-17 06:22:50.703934
# Keep-alive comment: 2025-06-17 17:22:19.264387
# Keep-alive comment: 2025-06-17 21:34:29.426051
# Keep-alive comment: 2025-06-18 04:22:26.069445
# Keep-alive comment: 2025-06-18 15:22:20.403322
# Keep-alive comment: 2025-06-19 02:22:24.008658
# Keep-alive comment: 2025-06-19 13:22:22.094507
# Keep-alive comment: 2025-06-20 00:22:20.538773
# Keep-alive comment: 2025-06-20 11:23:09.032977
# Keep-alive comment: 2025-06-20 22:22:29.366972
# Keep-alive comment: 2025-06-21 09:22:15.136988
# Keep-alive comment: 2025-06-21 20:22:26.890165
# Keep-alive comment: 2025-06-22 07:22:20.008109
# Keep-alive comment: 2025-06-22 18:22:10.509423
# Keep-alive comment: 2025-06-23 05:22:27.305172
# Keep-alive comment: 2025-06-23 16:22:19.062425
# Keep-alive comment: 2025-06-24 03:22:25.800693
# Keep-alive comment: 2025-06-24 14:22:03.810587
# Keep-alive comment: 2025-06-25 01:21:59.076477
# Keep-alive comment: 2025-06-25 12:22:20.119017
# Keep-alive comment: 2025-06-25 23:22:24.101497
# Keep-alive comment: 2025-06-26 10:22:31.513142
# Keep-alive comment: 2025-06-26 21:23:54.619549
# Keep-alive comment: 2025-06-27 08:22:24.822879
# Keep-alive comment: 2025-06-27 19:22:21.712946
# Keep-alive comment: 2025-06-28 06:22:29.995247
# Keep-alive comment: 2025-06-28 17:22:20.387042
# Keep-alive comment: 2025-06-29 04:22:09.270295
# Keep-alive comment: 2025-06-29 15:21:59.473716
# Keep-alive comment: 2025-06-30 02:22:21.298752
# Keep-alive comment: 2025-06-30 13:22:01.045583
# Keep-alive comment: 2025-07-01 00:24:06.388153
# Keep-alive comment: 2025-07-01 11:22:20.874837
# Keep-alive comment: 2025-07-01 22:22:25.916752
# Keep-alive comment: 2025-07-02 09:22:19.552142
# Keep-alive comment: 2025-07-02 20:24:08.037536
# Keep-alive comment: 2025-07-03 07:22:34.319055
# Keep-alive comment: 2025-07-03 18:21:58.165434
# Keep-alive comment: 2025-07-04 05:22:23.307182
# Keep-alive comment: 2025-07-04 16:22:19.154507
# Keep-alive comment: 2025-07-05 03:22:18.634440
# Keep-alive comment: 2025-07-05 14:22:24.311257
# Keep-alive comment: 2025-07-06 01:22:19.748943
# Keep-alive comment: 2025-07-06 12:22:18.634150
# Keep-alive comment: 2025-07-06 23:22:19.447611
# Keep-alive comment: 2025-07-07 10:22:18.860075
# Keep-alive comment: 2025-07-07 21:22:18.137898
# Keep-alive comment: 2025-07-08 08:22:23.349368
# Keep-alive comment: 2025-07-08 19:22:18.188927
# Keep-alive comment: 2025-07-09 06:22:30.231420
# Keep-alive comment: 2025-07-09 17:23:02.406339
# Keep-alive comment: 2025-07-10 04:22:19.117649
# Keep-alive comment: 2025-07-10 15:22:23.238777
# Keep-alive comment: 2025-07-11 02:22:18.048140
# Keep-alive comment: 2025-07-11 13:22:18.017761
# Keep-alive comment: 2025-07-12 00:22:04.641606
# Keep-alive comment: 2025-07-12 11:22:23.872378
# Keep-alive comment: 2025-07-12 22:22:19.002063
# Keep-alive comment: 2025-07-13 09:22:19.796363
# Keep-alive comment: 2025-07-13 20:22:03.975388
# Keep-alive comment: 2025-07-14 07:22:14.476904
# Keep-alive comment: 2025-07-14 18:22:37.972358
# Keep-alive comment: 2025-07-15 05:22:29.690491
# Keep-alive comment: 2025-07-15 16:22:22.885739
# Keep-alive comment: 2025-07-16 03:22:23.467295
# Keep-alive comment: 2025-07-16 14:22:22.861906
# Keep-alive comment: 2025-07-17 01:22:19.060415
# Keep-alive comment: 2025-07-17 12:22:24.341978
# Keep-alive comment: 2025-07-17 23:22:17.580489
# Keep-alive comment: 2025-07-18 10:22:38.207229
# Keep-alive comment: 2025-07-18 21:22:18.417102
# Keep-alive comment: 2025-07-19 08:22:59.354269
# Keep-alive comment: 2025-07-19 19:22:04.165772
# Keep-alive comment: 2025-07-20 06:22:29.016320
# Keep-alive comment: 2025-07-20 17:22:34.416746