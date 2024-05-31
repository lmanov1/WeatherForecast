# -*- coding: utf-8 -*-
from weatherforecast import *
import streamlit as st
import pandas as pd

def st_print_location(location,api_key):
    weather = print_city_weather(location, api_key)    
    
    if len(weather) == 1:
        st.write(f"No weather data found for {location}")
        st.write( weather)
        return
    # Create a DataFrame from the weather data  ,   location value as an index   
    df = pd.DataFrame(weather.items(), columns=[location.capitalize(), '']) 
        
    # CSS to inject contained in a string    
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # Display a static table
    st.table(df) 

def weather_at_city():    
    if st.session_state.city_name.lower() == "exit" or st.session_state.city_name.lower() == "quit":
        store_locations()
        st.write(".. Exiting...")
        st.stop()                                      
    else: 
        if len(st.session_state.city_name) == 0:                
            st.write("Please enter a valid city name")                
        else:
            st_print_location(st.session_state.city_name, st_api_key())                       


def get_and_process_city_name():
        
    if "city_name" not in st.session_state :
        st.session_state.city_name = ""
    
    city_name = st.text_input("Enter a city name (or 'exit' to quit): ", 
            on_change= weather_at_city(), key='city_name')
    

def st_api_key():
    """
    Reads the API key from the streamlite's secrets store and returns it.
    Returns:
        str: The API key.
    """
    if "openweathermap_api_key" in st.secrets:
        return st.secrets["openweathermap_api_key"]
    else:
        return st.text_input("Please enter your OpenWeatherMap API key: ")    
##############################################################################
       
def main():
    st.set_page_config(layout="wide")
    locations = read_locations()
    
    st.write("Weather at your stored locations")
    for location in locations:
        st_print_location(location , st_api_key())

    get_and_process_city_name()    

if __name__ == "__main__":
    main()