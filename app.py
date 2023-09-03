import datetime
import math
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from branca.element import Figure
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static
from dateutil.relativedelta import relativedelta
from data_collection import *
from predict import *
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time


st.set_page_config(
    page_title="Water Quality Monitoring Dashboard for Caspian Sea",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)


st.sidebar.markdown('<h1 style=" padding-top: 100px; margin-left:8%; color:black ">CASPIAN SEA Water Quality Monitoring Dashboard </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About the project", "Caspian Sea", "Analytics", "Conclusion")
)

if add_selectbox == 'Home':
    
    LOGO_IMAGE = "Caspian_Sea.jpg"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
             width:600px;
             height:650px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader('PROBLEM STATEMENT')
    
    st.markdown('Our objective is to create a web-based application that utilizes Remote Sensing and AI to enable the analysis, interpretation, and real-time visualization of various water quality parameters of Caspian Sea. The primary aim is to facilitate improved decision-making by identifying deviations from established standards, prompting immediate action when necessary, and enhancing overall water quality monitoring capabilities for the Caspian Sea.', 
         unsafe_allow_html=True)

    st.markdown(
          """
          <div class="container">
               <img class="logo-img" src="data:image/png;base64,{}">
          </div>
          """.format(base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()),
          unsafe_allow_html=True
    )
    
    

    
elif add_selectbox == 'About the project':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• Water Quality Indicators Dashboard for Analysis, Interpretation and Visualization near Real Time', unsafe_allow_html=True) 
    st.markdown('• Compare Real Water Quality Parameters with Standard Water Quality Limits', unsafe_allow_html=True) 
    
    st.markdown('<h4>Location</h4>', unsafe_allow_html=True)
    st.markdown('Caspian Sea region',unsafe_allow_html=True)
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown('• In our project we used most common water quality parameters which includes physical, biological and chemical parameters',unsafe_allow_html=True)
    st.markdown('• As a Data sources we used Google Earth Engine datasets and relevant sources were selected for future development.',unsafe_allow_html=True)
    st.markdown('• Analysed the images from the selected sources and applied various standard formulae were applied to analyse the colours of the &nbsp; water body regions.',unsafe_allow_html=True)
    st.markdown('• Final water quality parameters were selected and their names listed along with their band formulae.',unsafe_allow_html=True)
    st.markdown('• Several Machine learning models were applied on the final dataframe and the metrics were analysed and the best model was &nbsp; &nbsp; chosen with having a good validation accuracy.',unsafe_allow_html=True)
    st.markdown('• A dashboard is created for the public usage, every person could enter desired date range to &nbsp; get the water quality for interested area along with data visualisation of the collected data from the satellites.',unsafe_allow_html=True)


elif add_selectbox == 'Caspian Sea':

    st.subheader('The Caspian Sea')

    st.markdown('Caspian Sea, Russian Kaspiyskoye More, Persian Darya-ye Khezer, world’s largest inland body of water. It lies to the east of the Caucasus Mountains and to the west of the vast steppe of Central Asia. The sea’s name derives from the ancient Kaspi peoples, who once lived in Transcaucasia to the west. Among its other historical names, Khazarsk and Khvalynsk derive from former peoples of the region, while Girkansk stems from Girkanos, “Country of the Wolves.”', unsafe_allow_html=True)
    st.markdown('The elongated sea sprawls for nearly 750 miles (1,200 km) from north to south, although its average width is only 200 miles (320 km). It covers an area of about 149,200 square miles (386,400 square km)—larger than the area of Japan—and its surface lies some 90 feet (27 metres) below sea level. The maximum depth, toward the south, is 3,360 feet (1,025 metres) below the sea’s surface. The drainage basin of the sea covers some 1,400,000 square miles (3,625,000 square km). The sea contains some 63,400,000,000 acre-feet or 18,800 cubic miles (78,200 cubic km) of water—about one-third of Earth’s inland surface water. The sea is bordered in the northeast by Kazakhstan, in the southeast by Turkmenistan, in the south by Iran, in the southwest by Azerbaijan, and in the northwest by Russia.', unsafe_allow_html=True)
    st.markdown('The Caspian is the largest salt lake in the world, but that has not always been true. Scientific studies have shown that until relatively recent geologic times, approximately 11 million years ago, it was linked, via the Sea of Azov, the Black Sea, and the Mediterranean Sea, to the world ocean. The Caspian is of exceptional scientific interest, because its history—particularly former fluctuations in both area and depth—offers clues to the complex geologic and climatic evolution of the region. Human-made changes, notably those resulting from the construction of dams, reservoirs, and canals on the immense Volga River system (which drains into the Caspian from the north), have affected the contemporary hydrologic balance. Caspian shipping and fisheries play an important role in the region’s economy, as does the production of petroleum and natural gas in the Caspian basin. The sea’s splendid sandy beaches also serve as health and recreation resorts.', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Analytics':

   
    
    st.subheader('Analytics')    
    
    col1, col2 = st.columns(2)
    
    prm_type = col1.selectbox(
        "Data Visualization Parameters",
        ("All","pH","Salinity","Turbidity","Land Surface Temperature","Chlorophyll","Suspended matter",
     "Dissolved Organic Matter","Dissolved Oxygen")
    )

    lat = st.number_input('Latitude', min_value =43.44866,format="%.6f")

    long = st.number_input('Longitude',min_value=50.707414,  format="%.6f")

    
    
    col3,_ = st.columns((1,2)) # To make it narrower
    
    format = 'MMM DD, YYYY'  # format output
        
    start1 = datetime.date(year=2023,month=1,day=1)-relativedelta(years=1) #  I need some range in the past

    start2 = datetime.date(year=2023,month=11,day=1)
    st.text("")
    st.text("")
    
    st.write("Note-1:The difference between start date and end date should not exceed more than 3 months.")
    st.text("")
    st.text("")

    st.write("Note-2: The minimum difference between start date and end date should be 15 days.")
    st.text("")
    st.text("")
    
    max_days = start2-start1
        
    slider1 = col3.slider('Select Start Date', min_value=start1, value=start2 ,max_value=start2, format=format)
        ## Salinity check
    st.table(pd.DataFrame([[start1, slider1,start2]],
                      columns=['start1',
                               'start_selected',
                               'start2'],
                      index=['date']))

    end1 = datetime.date(year=2023,month=1,day=15)-relativedelta(years=1) #  I need some range in the past
    
    end2 = datetime.date(year=2023,month=12,day=31)
    
    max_days = end2-end1
        
    slider2 = col3.slider('Select End Date', min_value=end1, value=end2, max_value=end2, format=format)
        ## Salinity check
    st.table(pd.DataFrame([[end1, slider2, end2]],
                      columns=['end1',
                               'end_selected',
                               'end2'],
                      index=['date']))
    

    def plot_do(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(25,10))
        ax = sns.histplot(df_all['Dissolved Oxygen'], kde=True)
        # ax = sns.jointplot(data=df_all, x="Dissolved Oxygen", y="Value", hue="species")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Dissolved Oxygen'].min()), df_all['Dissolved Oxygen'].max() + 1, 0.5))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_dom(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(30,8))
        ax = sns.histplot(df_all['Dissolved Organic Matter'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Dissolved Organic Matter'].min()),df_all['Dissolved Organic Matter'].max() + 2, 20))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True) 
    
    def plot_salinity(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(20,8))
        ax = sns.histplot(df_all['Salinity'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Salinity'].min()),df_all['Salinity'].max() + 0.1, 0.01))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_turbidity(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(30,8))
        ax = sns.histplot(df_all['Turbidity'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Turbidity'].min()),df_all['Turbidity'].max() + 0.01, 0.3))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_temperature(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(30,8))
        ax = sns.histplot(df_all['Temperature'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Temperature'].min()),df_all['Temperature'].max() + 1, 0.5))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_chlorophyll(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(30,8))
        ax = sns.histplot(df_all['Chlorophyll'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Chlorophyll'].min()),df_all['Chlorophyll'].max() + 0.1, 0.01))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_pH(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(18,8))
        ax = sns.histplot(df_all['pH'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['pH'].min()), df_all['pH'].max() + 1, 0.1))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)

    def plot_sm(df_all):
        mpl.rcParams.update({"axes.grid" : True, "grid.color": "black"})
        sns.set(font_scale = 1)
        fig = plt.figure(figsize=(20,9))
        ax = sns.histplot(df_all['Suspended Matter'], kde=True, stat="density")
        ax.tick_params(axis='y', colors='black') 
        ax.tick_params(axis='x', colors='black') 
        # ax.set_xticks(np.arange(math.floor(df_all['Suspended Matter'].min()),df_all['Suspended Matter'].max() + 100, 20))
        plt.setp(ax.get_xticklabels(), rotation=-10)
        st.pyplot(fig, clear_figure = True)



    

    
    if st.button('Submit'):
        
        # try:
        st.text("")
        st.text("")
        st.write("Note-3: The location is pointed with a big black dot on the map, kindly magnify to view more.")
        st.text("")
        st.text("")
        df2 = get_data(long, lat, str(slider1), str(slider2))
        # st.text(print(df2.columns))
    
        st.text("")
        st.text("")

        #st.write(df2)
        df_all, test = send_df(df2)
        st.text("")
        st.text("")
        st.text("")
        # st.write(predict_quality(df2, test))
    

    
        st.text("")
        st.text("")
        st.text("")
        

        if prm_type == 'Dissolved Oxygen':
            plot_do(df_all)
        elif prm_type == 'Salinity':
            plot_salinity(df_all)
        elif prm_type == 'Land Surface Temperature':
            plot_temperature(df_all)
        elif prm_type == 'Turbidity':
            plot_turbidity(df_all)
        elif prm_type == 'pH':
            plot_pH(df_all)
        elif prm_type == 'Chlorophyll':
            plot_chlorophyll(df_all)
        elif prm_type == 'Suspended Matter':
            plot_sm(df_all)
        elif prm_type == 'Dissolved Organic Matter':
            plot_dom(df_all)
        else:
            plot_dom(df_all)
            plot_pH(df_all)
            plot_sm(df_all)
            plot_chlorophyll(df_all)
            plot_turbidity(df_all)
            plot_temperature(df_all)
            plot_salinity(df_all)
            plot_do(df_all)
        # except:
        #     st.write("!!  Enter proper date range  !!") 
    
elif add_selectbox == 'Conclusion':

    st.subheader('Project technical part')

    st.markdown('• Data Collection - Google Earth Datasets', unsafe_allow_html=True)
    st.markdown('• Data Visualization - Google Earth Engine, Python libraries', unsafe_allow_html=True)
    st.markdown('• Satellite Imagery Analysis - Google Earth Engine', unsafe_allow_html=True) 
    st.markdown('• Machine Learning - Python, Jupyter Notebooks', unsafe_allow_html=True) 
    st.markdown('• Dashboard - Streamlit, Vercel', unsafe_allow_html=True) 

    st.subheader('PROJECT SUMMARY')

    st.markdown('', unsafe_allow_html=True) 
    st.markdown('• Water quality is one of the main challenges that societies are facing in the 21st century, threatening human health, limiting food production, reducing ecosystem functions, and hindering economic growth. It corrupts straightforwardly into ecological, financial, and social issues.', unsafe_allow_html=True) 
    st.markdown('• This dashboard will reinforce the abilities of decision-makers to monitor water quality more effectively and efficiently.', unsafe_allow_html=True) 
    st.markdown('• As the traditional in situ method is costly as well as time-consuming so using advanced geospatial technology water quality can be monitored spatially and temporally in near real- time and self-operating.', unsafe_allow_html=True) 
    
 