import streamlit as st
import pandas as pd
import json as js 
import requests as rq
from PIL import Image

airport_name = ""
airport_code = ""

# Create the airport lookup df 
airport_lookup = pd.read_csv("airport_codes.csv")

# Title
st.markdown("<h1 style='text-align: center; font-size: 40px; font-family: Arial;'>Current Weather at an European Airport</h1>", unsafe_allow_html=True)
#st.set_page_config(layout="wide", initial_sidebar_state="expanded", backgroundColor="#F5F5F5")
#st.markdown("<style> body {background-color: #F5F5F5;}</style>", unsafe_allow_html=True)

# Banner image
img = Image.open("Airplane_banner.png")
st.image(img, width=900)



# Create the input form
if __name__ == "__main__":
    # Create the customer data input form 
    with st.sidebar:
        st.subheader("Please select the country and airport from the dropdown menus below.")
        with st.form("form1"):
            country = st.selectbox('Country?',options=['select']+list(airport_lookup['Country'].unique()))
            submit_button_country = st.form_submit_button(label='Submit Country')
            if country != 'select': 
                airport = st.selectbox('Airport?',options=['select']+list(airport_lookup[airport_lookup['Country']==country]['Airport'].unique()))
                submit_button_airport = st.form_submit_button(label='Submit Airport')
                if airport != 'select':    
                    airport_code = airport_lookup[airport_lookup['Airport']==airport]['ICAO'].values[0]
                    airport_name = airport_lookup[airport_lookup['Airport']==airport]['Airport'].values[0]
            # Create a reset button
            # reset = st.form_submit_button("Reset")
            # if reset:
            #     st.session_state.airport = 'select'
            #     st.session_state.country = 'select'
            # Create a reset button

            

# Use the airport code to get the weather data from the API
if airport_name and airport_code:
    api_resp = rq.get("https://api.aviationapi.com/v1/weather/metar?apt="+airport_code)
    data = api_resp.json()
    allKeys = data.keys()
    if 'status' in allKeys:
        st.error("No weather data available for "+airport_code+".")
    else:
        st.success("Current weather at "+airport+'('+airport_code+')')
        # Create columns for output
        col1, col2 = st.columns(2)

        # Add content to the columns
        with col1:
            st.write("Temperature: "+str(data[airport_code]['temp'])+" C")
            st.write("Wind speed: "+str(data[airport_code]['wind_vel'])+" m/s")
            st.write("Wind direction: "+str(data[airport_code]['wind'])+" degrees")
            
        with col2:
            st.write("Visibility: "+str(data[airport_code]['visibility'])+" %")
            st.write("Pressure: "+str(data[airport_code]['alt_hg'])+" hPa")
            st.write("Dew Point: "+str(data[airport_code]['dewpoint'])+" C")



