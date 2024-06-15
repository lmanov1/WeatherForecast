# -*- coding: utf-8 -*-
from weatherforecast import *
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import pytz
import datetime

st.set_page_config(layout="wide")
local_time_text = st.empty()


def st_print_location(location, api_key):
    """
    Prints the weather information for a given location.

    Args:
        location (str): The name of the location.
        api_key (str): The API key for accessing weather data.

    Returns:
        None
    """
    weather = print_city_weather(location, api_key)
    # Check if error description
    if len(weather) == 1:
        st.write(f"No weather data found for \"{location}\"")
        st.write(weather.popitem()[1])
        return
    if location in locations.keys():  
        container = st.container( height=480, border=True)
        with container:
            cols = st.columns(2,gap="medium")
            with cols[0]:                          
                weather['Country'] = locations[location]['country']
                weather_image = weather['Image']            
                st.image(f"https://openweathermap.org/img/wn/{weather_image}@2x.png", width=60 )
                weather.pop('Image') # no more need
                
                df = pd.DataFrame(weather.items(), columns=[location.title(),''])
                hide_table_row_index = """
                            <style>
                            tbody th {display:none}
                            .blank {display:none}
                            </style>
                            """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(df)
            with cols[1]:
                
                curr_coord = dict(locations[location])
                map_data = pd.DataFrame({
                        'latitude': [curr_coord['lat']],
                        'longitude': [curr_coord['lon']]
                    })
                map_container = st.container(height=450,border=False)
                with map_container:
                    ## Create a map with the data
                    st.map(map_data, size=300, color='#0044ff',zoom = 10)                
                
                   
                

def weather_at_city():
    """
    Handles the weather information for a given city.

    Returns:
        None
    """
    if len(st.session_state.city_name) != 0:
        st_print_location(st.session_state.city_name, st_api_key())
    else:
        pass

def get_and_process_city_name():
    """
    Gets and processes the city name entered by the user.

    Returns:
        None
    """
    if "city_name" not in st.session_state:
        st.session_state.city_name = ""

    city_name = st.text_input("Enter city name",
                on_change = weather_at_city(), key='city_name')

def st_api_key():
    """
    Reads the API key from the streamlite's secrets store and returns it to a calling function.

    Returns:
        str: The API key.
    """
    if "openweathermap_api_key" in st.secrets:
        return decode_string(st.secrets["openweathermap_api_key"])
    else:
        return st.text_input("Please enter your OpenWeatherMap API key: ")

def checkbox_container(data):
    """
    Manages the checkboxes for storing and removing locations.

    Args:
        data (list): List of locations.

    Returns:
        None
    """
    new_data = st.text_input('Enter new location to store')
    cols = st.columns(4)
    if cols[0].button('Add location'):
        data.append(new_data.title())
        print_city_weather(new_data.lower(), st_api_key())
        store_locations()
    if cols[1].button('Select All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = True
    if cols[2].button('UnSelect All'):
        for i in data:
            st.session_state['dynamic_checkbox_' + i] = False
    if cols[3].button('Remove Selected'):
        to_remove = []
        for i in data:
            if st.session_state['dynamic_checkbox_' + i] == True:
                if i.lower() in locations.keys():
                    locations.pop(i.lower())
                    store_locations()
                    to_remove.append(i)
                else:
                    st.write(f"Location {i} not found in stored locations")

        for i in to_remove:
            data.remove(i)

    for i in data:
        st.checkbox(i, key='dynamic_checkbox_' + i)

def get_selected_checkboxes():
    """
    Gets the currently selected checkboxes in checkboxes container

    Returns:
        list: List of selected checkboxes.
    """
    return [i.replace('dynamic_checkbox_', '') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]

def manage_locations():
    """
    Manages the stored locations.

    Returns:
        None
    """
    locations = read_locations()
    locations_data_names = [location.title() for location in locations.keys()]

    if 'locations_data' in st.session_state.keys():
        del st.session_state['locations_data']
    st.session_state['locations_data'] = locations_data_names

    checkbox_container(locations_data_names)

def save_timezone():
    """
    Saves the user's local timezone.

    Returns:
        None
    """
    st.write("Enter your local timezone")
    timezone_options = pytz.all_timezones
    saved_timezone = read_conf('timezone')

    selected_timezone = st.selectbox("Select your timezone", timezone_options, timezone_options.index(saved_timezone))
    if st.button("Save"):
        store_conf('timezone', selected_timezone)
        local_time_text.text(f"{print_time_for_stored_timezone()}")

def change_preferences():
    """
    Changes the user's preferred units type.

    Returns:
        None
    """
    st.write("Enter your preferred units type")
    temp_units = ["Celsius", "Fahrenheit"]
    selected_unit = st.selectbox("Select your preferred units", temp_units, index=temp_units.index(read_conf('units')))
    if st.button("Save"):
        store_conf('units', selected_unit)

configuration_options = ["Chose one option below", "Manage stored locations", "Enter your preferred metrics", "Enter your local timezone"]

def process_selection():
    """
    Processes the selected option from the settings menu.

    Returns:
        None
    """
    if st.session_state.selected_option == "Manage stored locations":
        manage_locations()
    elif st.session_state.selected_option == "Enter your preferred metrics":
        change_preferences()
    elif st.session_state.selected_option == "Enter your local timezone":
        save_timezone()

def process_settings():
    """
    Processes the settings menu.

    Returns:
        None
    """
    st.title("Weather settings")
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = configuration_options[0]

    hor_line = '⎯'*30 # separator line
    st.selectbox(
        f'{hor_line} **Select one of the following** {hor_line}',
        configuration_options,
        key='selected_option', on_change=process_selection(),       
        placeholder="Select a settings option...",
    )

def main():
    """
    Main function to run the Sreamlit-based Weather Watchdog application.

    Returns:
        None
    """
    locations = read_locations()

    with st.sidebar:
        st.image("./Sun_Wave_Logo_T.png", width=150)

        side_bar_options= ['My cities', 'Settings']
        selected = option_menu(
            menu_title=f"",
            options = side_bar_options,
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": "orange", "font-size": "16px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "fee0e3"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    local_time_text.text(print_time_for_stored_timezone())

    if selected == "My cities":        
        if len(locations) == 0:
            st.write("No locations currently stored , please add some")
        else:
            st.write("Would you like to add another location?")

        get_and_process_city_name()
        for location in locations:
            st_print_location(location, st_api_key())

        store_locations()
    elif selected == "Settings":
        process_settings()

if __name__ == "__main__":
    main()
