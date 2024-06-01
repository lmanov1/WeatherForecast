# -*- coding: utf-8 -*-
from weatherforecast import *
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import pytz
import datetime

####      Helper functions     ####
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

    city_name = st.text_input("Enter city name (or 'exit' to quit) ",
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

##### Settings  ####


def checkbox_container(data):
    new_data = st.text_input('Enter new location to store')
    cols = st.columns(4)
    if cols[0].button('Add location'):
        data.append(new_data.capitalize())
        print_city_weather(new_data.lower(), st_api_key())
        store_locations()
    if cols[1].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
    if cols[2].button('UnSelect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
    if cols[3].button('Remove Selected'):
        for i in data:
            if st.session_state['dynamic_checkbox_' + i] == True:
                if i.lower() in locations.keys():
                    locations.pop(i.lower())
                    store_locations()
                    data.remove(i)
                else:
                    st.write(f"Location {i} not found in stored locations")
    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)

def get_selected_checkboxes():
    return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def manage_locations():
    locations = read_locations()

    if 'locations_data' not in st.session_state.keys():
        locations_data = [ location.capitalize() for location in locations.keys()]
        st.session_state['locations_data'] = locations_data
    else:
        locations_data = st.session_state['locations_data']

    checkbox_container(locations_data)
    #st.write('You selected:')
    #st.write(get_selected_checkboxes())

def save_timezone():
    st.write("Enter your local timezone")
    timezone_options = pytz.all_timezones
    selected_timezone = st.selectbox("Select your timezone", timezone_options)
    store_timezone(selected_timezone)
    st.write(f"Local time: {print_time_for_stored_timezone()}")



configuration_options = ["Manage stored locations", "Change API key", "Enter your preferred metrics", "Enter your local timezone"]
def process_selection():
    
    if st.session_state.selected_option == "Manage stored locations":
        manage_locations()
    elif st.session_state.selected_option == "Change API key":
        st.write("Change API key")
    elif st.session_state.selected_option == "Enter your preferred metrics":
        st.write("Enter your preferred metrics")
    elif st.session_state.selected_option == "Enter your local timezone":
        save_timezone()



def process_settings():
    st.title("Weather settings")
    if "selected_option" not in st.session_state :
        st.session_state.selected_option = configuration_options[0]

    hor_line = '⎯'*30
    st.selectbox(
        f'{hor_line} **Select one of the following** {hor_line}',
        configuration_options,
        key='selected_option', on_change= process_selection() ,
        #index=0,
        placeholder="Select a settings option...",
    )


##############################################################################

def main():
    #st.set_page_config(layout="wide")
    locations = read_locations()

    with st.sidebar:
        st.image("./Sun_Wave_Logo_T.png",width=150)
        st.text(print_time_for_stored_timezone())

        selected = option_menu(
            menu_title=f"",
            options=["Enter a city name", "History", "Settings", "Exit"],
            default_index=0,
            orientation="vertical",
             styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "orange", "font-size": "16px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "fee0e3"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    if selected == "Enter a city name":
        get_and_process_city_name()
    elif selected == "History":
        st.write("Weather at your stored locations")
        for location in locations:
            st_print_location(location , st_api_key())
    elif selected == "Settings":
        process_settings()
    elif selected == "Exit":
        store_locations()
        st.write(".. Bye-bye...See you soon")
        st.stop()



if __name__ == "__main__":
    main()