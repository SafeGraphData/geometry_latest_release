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
# Keep-alive comment: 2025-07-21 04:22:29.067357
# Keep-alive comment: 2025-07-21 15:22:13.961736
# Keep-alive comment: 2025-07-22 02:22:38.057770
# Keep-alive comment: 2025-07-22 13:22:50.061603
# Keep-alive comment: 2025-07-23 00:22:25.148169
# Keep-alive comment: 2025-07-23 11:22:13.753333
# Keep-alive comment: 2025-07-23 22:22:17.881328
# Keep-alive comment: 2025-07-24 09:22:33.579922
# Keep-alive comment: 2025-07-24 20:22:19.242310
# Keep-alive comment: 2025-07-25 07:22:13.683671
# Keep-alive comment: 2025-07-25 18:22:17.921945
# Keep-alive comment: 2025-07-26 05:22:14.764273
# Keep-alive comment: 2025-07-26 16:22:18.406981
# Keep-alive comment: 2025-07-27 03:22:13.887906
# Keep-alive comment: 2025-07-27 14:22:04.236795
# Keep-alive comment: 2025-07-28 01:22:24.517097
# Keep-alive comment: 2025-07-28 12:22:19.310270
# Keep-alive comment: 2025-07-28 23:22:18.064818
# Keep-alive comment: 2025-07-29 10:21:52.874077
# Keep-alive comment: 2025-07-29 21:22:23.462282
# Keep-alive comment: 2025-07-30 08:22:19.796690
# Keep-alive comment: 2025-07-30 19:22:27.986987
# Keep-alive comment: 2025-07-31 06:22:32.960551
# Keep-alive comment: 2025-07-31 17:22:18.843892
# Keep-alive comment: 2025-08-01 04:22:18.180296
# Keep-alive comment: 2025-08-01 15:22:28.262781
# Keep-alive comment: 2025-08-02 02:22:14.042881
# Keep-alive comment: 2025-08-02 13:22:24.366526
# Keep-alive comment: 2025-08-03 00:22:19.560494
# Keep-alive comment: 2025-08-03 11:22:24.436097
# Keep-alive comment: 2025-08-03 22:22:18.935151
# Keep-alive comment: 2025-08-04 09:22:14.843128
# Keep-alive comment: 2025-08-04 20:22:18.277295
# Keep-alive comment: 2025-08-05 07:22:21.656881
# Keep-alive comment: 2025-08-05 18:22:22.601994
# Keep-alive comment: 2025-08-06 05:22:18.720070
# Keep-alive comment: 2025-08-06 16:24:08.531395
# Keep-alive comment: 2025-08-07 03:22:22.981164
# Keep-alive comment: 2025-08-07 14:22:23.434976
# Keep-alive comment: 2025-08-08 01:22:13.038806
# Keep-alive comment: 2025-08-08 12:22:23.851252
# Keep-alive comment: 2025-08-08 23:22:24.897460
# Keep-alive comment: 2025-08-09 10:22:18.908895
# Keep-alive comment: 2025-08-09 21:22:40.180917
# Keep-alive comment: 2025-08-10 08:22:24.814663
# Keep-alive comment: 2025-08-10 19:22:24.855641
# Keep-alive comment: 2025-08-11 06:22:18.672736
# Keep-alive comment: 2025-08-11 17:22:23.528105
# Keep-alive comment: 2025-08-12 04:22:23.059435
# Keep-alive comment: 2025-08-12 15:22:13.628550
# Keep-alive comment: 2025-08-13 02:22:23.265446
# Keep-alive comment: 2025-08-13 13:22:17.929799
# Keep-alive comment: 2025-08-14 00:22:17.688403
# Keep-alive comment: 2025-08-14 11:22:24.151857
# Keep-alive comment: 2025-08-14 22:22:18.128949
# Keep-alive comment: 2025-08-15 09:22:18.039069
# Keep-alive comment: 2025-08-15 20:22:07.702455
# Keep-alive comment: 2025-08-16 07:22:33.284494
# Keep-alive comment: 2025-08-16 18:22:18.261168
# Keep-alive comment: 2025-08-17 05:22:23.033172
# Keep-alive comment: 2025-08-17 16:22:18.022589
# Keep-alive comment: 2025-08-18 03:22:18.956420
# Keep-alive comment: 2025-08-18 14:22:18.123405
# Keep-alive comment: 2025-08-19 01:22:18.774076
# Keep-alive comment: 2025-08-19 12:22:23.127603
# Keep-alive comment: 2025-08-19 23:22:45.609817
# Keep-alive comment: 2025-08-20 10:22:18.252181
# Keep-alive comment: 2025-08-20 21:22:22.980319
# Keep-alive comment: 2025-08-21 08:22:19.867832
# Keep-alive comment: 2025-08-21 19:22:23.772449
# Keep-alive comment: 2025-08-22 06:22:23.823566
# Keep-alive comment: 2025-08-22 17:22:18.602270
# Keep-alive comment: 2025-08-23 04:22:28.991569
# Keep-alive comment: 2025-08-23 15:22:18.148803
# Keep-alive comment: 2025-08-24 02:22:17.824469
# Keep-alive comment: 2025-08-24 13:22:18.723364
# Keep-alive comment: 2025-08-25 00:22:24.378357
# Keep-alive comment: 2025-08-25 11:22:23.388150
# Keep-alive comment: 2025-08-25 22:22:18.351012
# Keep-alive comment: 2025-08-26 09:22:18.260837
# Keep-alive comment: 2025-08-26 20:22:22.692785
# Keep-alive comment: 2025-08-27 07:22:28.239736
# Keep-alive comment: 2025-08-27 18:21:57.695006
# Keep-alive comment: 2025-08-28 05:22:28.996650
# Keep-alive comment: 2025-08-28 16:22:17.862417
# Keep-alive comment: 2025-08-29 03:22:03.031871
# Keep-alive comment: 2025-08-29 14:22:07.953305
# Keep-alive comment: 2025-08-30 01:22:08.272452
# Keep-alive comment: 2025-08-30 12:22:04.085171
# Keep-alive comment: 2025-08-30 23:22:07.678166
# Keep-alive comment: 2025-08-31 10:22:03.019829
# Keep-alive comment: 2025-08-31 21:22:14.568238
# Keep-alive comment: 2025-09-01 08:22:14.787351
# Keep-alive comment: 2025-09-01 19:22:14.746600
# Keep-alive comment: 2025-09-02 06:22:03.002803
# Keep-alive comment: 2025-09-02 17:22:13.699160
# Keep-alive comment: 2025-09-03 04:22:07.772706
# Keep-alive comment: 2025-09-03 15:22:08.294980
# Keep-alive comment: 2025-09-04 02:22:13.308015
# Keep-alive comment: 2025-09-04 13:22:15.385153
# Keep-alive comment: 2025-09-05 00:22:04.213677
# Keep-alive comment: 2025-09-05 11:21:58.653026
# Keep-alive comment: 2025-09-05 22:22:08.258595
# Keep-alive comment: 2025-09-06 09:22:05.007890
# Keep-alive comment: 2025-09-06 20:22:03.223983
# Keep-alive comment: 2025-09-07 07:22:09.688088
# Keep-alive comment: 2025-09-07 18:22:09.245069
# Keep-alive comment: 2025-09-08 05:22:05.241913
# Keep-alive comment: 2025-09-08 16:22:08.358446
# Keep-alive comment: 2025-09-09 03:22:33.689011
# Keep-alive comment: 2025-09-09 14:22:08.153454
# Keep-alive comment: 2025-09-10 01:22:03.010672
# Keep-alive comment: 2025-09-10 12:22:13.528830
# Keep-alive comment: 2025-09-10 15:52:45.096326
# Keep-alive comment: 2025-09-10 23:22:03.203166
# Keep-alive comment: 2025-09-11 10:22:05.564844
# Keep-alive comment: 2025-09-11 21:22:03.848721
# Keep-alive comment: 2025-09-12 08:22:18.055016
# Keep-alive comment: 2025-09-12 19:22:08.622488
# Keep-alive comment: 2025-09-13 06:21:58.406595
# Keep-alive comment: 2025-09-13 17:22:04.868458
# Keep-alive comment: 2025-09-14 04:21:54.562583
# Keep-alive comment: 2025-09-14 15:22:05.910299
# Keep-alive comment: 2025-09-15 02:22:03.411164
# Keep-alive comment: 2025-09-15 13:22:04.093720
# Keep-alive comment: 2025-09-16 00:22:03.887240
# Keep-alive comment: 2025-09-16 11:22:08.183692
# Keep-alive comment: 2025-09-16 22:22:02.833606
# Keep-alive comment: 2025-09-17 09:22:04.328046
# Keep-alive comment: 2025-09-17 20:22:13.490045
# Keep-alive comment: 2025-09-18 07:22:10.349809
# Keep-alive comment: 2025-09-18 18:22:09.419898
# Keep-alive comment: 2025-09-19 05:22:04.916084
# Keep-alive comment: 2025-09-19 16:22:38.229325
# Keep-alive comment: 2025-09-20 03:22:09.388562
# Keep-alive comment: 2025-09-20 14:22:09.942330
# Keep-alive comment: 2025-09-21 01:22:09.265366
# Keep-alive comment: 2025-09-21 12:22:09.081612
# Keep-alive comment: 2025-09-21 23:22:04.399750
# Keep-alive comment: 2025-09-22 10:22:04.398845
# Keep-alive comment: 2025-09-22 21:22:02.744289
# Keep-alive comment: 2025-09-23 08:22:04.081066
# Keep-alive comment: 2025-09-23 19:22:09.178117
# Keep-alive comment: 2025-09-24 06:22:03.038785
# Keep-alive comment: 2025-09-24 17:22:07.839908
# Keep-alive comment: 2025-09-25 04:22:13.485700
# Keep-alive comment: 2025-09-25 15:22:12.901351
# Keep-alive comment: 2025-09-26 02:22:09.175252
# Keep-alive comment: 2025-09-26 13:22:13.111046
# Keep-alive comment: 2025-09-26 19:30:40.331981
# Keep-alive comment: 2025-09-27 05:30:46.742982
# Keep-alive comment: 2025-09-27 15:30:40.894920
# Keep-alive comment: 2025-09-28 01:30:45.269659
# Keep-alive comment: 2025-09-28 11:30:46.131535
# Keep-alive comment: 2025-09-28 21:30:45.582304
# Keep-alive comment: 2025-09-29 07:30:51.046258
# Keep-alive comment: 2025-09-29 17:31:01.123443
# Keep-alive comment: 2025-09-30 03:30:40.204875
# Keep-alive comment: 2025-09-30 13:30:45.675646
# Keep-alive comment: 2025-09-30 23:31:05.389879
# Keep-alive comment: 2025-10-01 09:31:11.410103
# Keep-alive comment: 2025-10-01 19:30:45.473098
# Keep-alive comment: 2025-10-02 05:31:14.991870
# Keep-alive comment: 2025-10-02 15:31:11.088305
# Keep-alive comment: 2025-10-03 01:30:45.355161
# Keep-alive comment: 2025-10-03 11:31:06.017840
# Keep-alive comment: 2025-10-03 21:30:40.340241
# Keep-alive comment: 2025-10-04 07:30:41.373582
# Keep-alive comment: 2025-10-04 17:30:50.669928
# Keep-alive comment: 2025-10-05 03:30:46.409416
# Keep-alive comment: 2025-10-05 13:30:50.976086
# Keep-alive comment: 2025-10-05 23:31:11.487597
# Keep-alive comment: 2025-10-06 09:31:16.083477
# Keep-alive comment: 2025-10-06 19:30:45.657302
# Keep-alive comment: 2025-10-07 05:30:47.750394
# Keep-alive comment: 2025-10-07 15:31:07.988455
# Keep-alive comment: 2025-10-08 01:30:46.401192
# Keep-alive comment: 2025-10-08 11:30:46.813343
# Keep-alive comment: 2025-10-08 21:30:45.951922
# Keep-alive comment: 2025-10-09 07:30:47.932430
# Keep-alive comment: 2025-10-09 17:30:47.446435
# Keep-alive comment: 2025-10-10 03:30:36.757264
# Keep-alive comment: 2025-10-10 13:30:26.710429
# Keep-alive comment: 2025-10-10 23:30:41.157673
# Keep-alive comment: 2025-10-11 09:30:46.962611
# Keep-alive comment: 2025-10-11 19:30:40.561893
# Keep-alive comment: 2025-10-12 05:30:43.785862
# Keep-alive comment: 2025-10-12 15:30:47.924798
# Keep-alive comment: 2025-10-13 01:30:42.503671
# Keep-alive comment: 2025-10-13 11:31:13.302668
# Keep-alive comment: 2025-10-13 21:30:36.728643
# Keep-alive comment: 2025-10-14 07:30:40.403386
# Keep-alive comment: 2025-10-14 17:30:42.163957
# Keep-alive comment: 2025-10-15 03:30:40.895356
# Keep-alive comment: 2025-10-15 13:30:40.884846
# Keep-alive comment: 2025-10-15 23:30:46.129345
# Keep-alive comment: 2025-10-16 09:30:41.131140
# Keep-alive comment: 2025-10-16 19:30:46.946286
# Keep-alive comment: 2025-10-17 05:30:46.355497
# Keep-alive comment: 2025-10-17 15:31:02.087525
# Keep-alive comment: 2025-10-18 01:30:42.357718
# Keep-alive comment: 2025-10-18 11:31:07.403204
# Keep-alive comment: 2025-10-18 21:31:17.316734
# Keep-alive comment: 2025-10-19 07:30:36.989639
# Keep-alive comment: 2025-10-19 17:31:11.903156
# Keep-alive comment: 2025-10-20 03:31:08.466673
# Keep-alive comment: 2025-10-20 13:30:46.418448
# Keep-alive comment: 2025-10-20 23:30:41.658925
# Keep-alive comment: 2025-10-21 09:30:47.055905
# Keep-alive comment: 2025-10-21 19:32:46.357884
# Keep-alive comment: 2025-10-22 05:30:42.743436
# Keep-alive comment: 2025-10-22 15:31:46.711629
# Keep-alive comment: 2025-10-23 01:30:41.902381
# Keep-alive comment: 2025-10-23 11:30:53.832094
# Keep-alive comment: 2025-10-23 21:30:42.515044
# Keep-alive comment: 2025-10-24 07:32:02.262912
# Keep-alive comment: 2025-10-24 17:30:52.122775
# Keep-alive comment: 2025-10-25 03:30:47.704098
# Keep-alive comment: 2025-10-25 13:31:11.653770
# Keep-alive comment: 2025-10-25 23:30:42.361703
# Keep-alive comment: 2025-10-26 09:30:37.194079
# Keep-alive comment: 2025-10-26 19:31:13.520733
# Keep-alive comment: 2025-10-27 05:30:53.429162
# Keep-alive comment: 2025-10-27 15:31:06.638475
# Keep-alive comment: 2025-10-28 01:30:46.096778
# Keep-alive comment: 2025-10-28 11:30:47.176344
# Keep-alive comment: 2025-10-28 21:30:36.501469
# Keep-alive comment: 2025-10-29 07:30:43.406423
# Keep-alive comment: 2025-10-29 17:30:51.444215
# Keep-alive comment: 2025-10-30 03:30:42.319761
# Keep-alive comment: 2025-10-30 13:31:12.979081
# Keep-alive comment: 2025-10-30 23:30:47.539031
# Keep-alive comment: 2025-10-31 09:32:02.850577
# Keep-alive comment: 2025-10-31 19:30:38.494863
# Keep-alive comment: 2025-11-01 05:30:47.354638
# Keep-alive comment: 2025-11-01 15:30:36.707827
# Keep-alive comment: 2025-11-02 01:30:47.124248
# Keep-alive comment: 2025-11-02 11:30:48.505771
# Keep-alive comment: 2025-11-02 21:31:03.846429
# Keep-alive comment: 2025-11-03 07:30:42.898769
# Keep-alive comment: 2025-11-03 17:30:46.515459
# Keep-alive comment: 2025-11-04 03:30:47.478023
# Keep-alive comment: 2025-11-04 13:31:13.964491
# Keep-alive comment: 2025-11-04 23:31:06.108663
# Keep-alive comment: 2025-11-05 09:31:17.259320
# Keep-alive comment: 2025-11-05 19:30:46.586304
# Keep-alive comment: 2025-11-06 05:31:13.041415
# Keep-alive comment: 2025-11-06 15:30:59.111332
# Keep-alive comment: 2025-11-07 01:30:45.063033
# Keep-alive comment: 2025-11-07 11:30:47.767309
# Keep-alive comment: 2025-11-07 21:30:48.221770
# Keep-alive comment: 2025-11-08 07:30:37.690431
# Keep-alive comment: 2025-11-08 17:30:53.521631
# Keep-alive comment: 2025-11-09 03:31:27.509294
# Keep-alive comment: 2025-11-09 13:30:48.252118
# Keep-alive comment: 2025-11-09 23:30:37.965395
# Keep-alive comment: 2025-11-10 09:30:42.505730
# Keep-alive comment: 2025-11-10 19:30:57.822968
# Keep-alive comment: 2025-11-11 05:30:44.041608
# Keep-alive comment: 2025-11-11 15:30:41.179423
# Keep-alive comment: 2025-11-12 01:30:49.412670
# Keep-alive comment: 2025-11-12 11:30:50.420027
# Keep-alive comment: 2025-11-12 21:31:07.371854
# Keep-alive comment: 2025-11-13 07:30:30.066325
# Keep-alive comment: 2025-11-13 17:30:42.405015
# Keep-alive comment: 2025-11-14 03:30:50.185714
# Keep-alive comment: 2025-11-14 13:31:10.599923
# Keep-alive comment: 2025-11-14 23:30:43.028016
# Keep-alive comment: 2025-11-15 09:30:47.452754
# Keep-alive comment: 2025-11-15 19:30:52.981161
# Keep-alive comment: 2025-11-16 05:30:43.682141
# Keep-alive comment: 2025-11-16 15:30:48.840192
# Keep-alive comment: 2025-11-17 01:30:37.933686
# Keep-alive comment: 2025-11-17 11:31:12.014216
# Keep-alive comment: 2025-11-17 21:30:37.611588
# Keep-alive comment: 2025-11-18 07:30:42.413123
# Keep-alive comment: 2025-11-18 17:30:41.560555
# Keep-alive comment: 2025-11-19 03:30:47.014404
# Keep-alive comment: 2025-11-19 13:30:37.792749
# Keep-alive comment: 2025-11-19 23:30:41.332389
# Keep-alive comment: 2025-11-20 09:30:47.671020
# Keep-alive comment: 2025-11-20 19:32:37.503291
# Keep-alive comment: 2025-11-21 05:30:43.570132