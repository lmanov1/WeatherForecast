# -*- coding: utf-8 -*-
from weatherforecast import *
import streamlit as st
import pandas as pd

def st_print_location(location,api_key):
    weather_str = print_city_weather(location, api_key)    
    weather_data = weather_str.split("\n")
    #print(weather_data)
    if len(weather_data) == 1:
        st.write(f"No weather data found for {location}")
        st.write( weather_data)
        return
    # Create a DataFrame from the weather data  ,   weather_data[1:] as an index   
    df = pd.DataFrame(weather_data[1:], columns=[weather_data[0]])  
    
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


def st_print_weather_with_units(weather_dict, units_dict, 
                             remote_utc_timestamp = None, 
                             datetime_print_format="%A, %B %d, %Y, %I:%M %p", 
                             remote_tz_shift_secs = None):
    
    answer = print_weather_with_units(weather_dict, units_dict, 
                             remote_utc_timestamp, 
                             datetime_print_format, 
                             remote_tz_shift_secs)    
    st.write(answer)    

def weather_at_city():    
    if st.session_state.city_name.lower() == "exit" or st.session_state.city_name.lower() == "quit":
        store_locations()
        st.write(".. Exiting...")
        st.stop()                                      
    else: 
        if len(st.session_state.city_name) == 0:                
            st.write("Please enter a valid city name")                
        else:
            st_print_location(st.session_state.city_name, my_api_key())                       


def get_and_process_city_name():
        
    if "city_name" not in st.session_state :
        st.session_state.city_name = ""
    
    city_name = st.text_input("Enter a city name (or 'exit' to quit): ", 
            on_change= weather_at_city(), key='city_name')
    

##############################################################################
       
def main():
    st.set_page_config(layout="wide")
    locations = read_locations()
    
    st.write("Weather at your stored locations")
    for location in locations:
        st_print_location(location , my_api_key())

    get_and_process_city_name()    

if __name__ == "__main__":
    main()