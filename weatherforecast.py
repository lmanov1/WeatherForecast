# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime , timedelta
import pytz
import sys
import tomlkit
from pathlib import Path

############################### Global definitions ####################################
conf_file_name = "./.streamlit/conf.toml"
exclude_list = ["icon", "id"]
locations = {}
units = "metric"

location_settings = {
    "coord":["lon","lat"],
    "sys": ["country"],
    "timezone": "timezone"
}

# TBD: display icon from url : https://openweathermap.org/img/wn/{icon}}@2x.png
weather_api = ["weather", "main"
               #"visibility" , "wind", "clouds", "rain", "snow"
              ]

weather_api1 = {
        "weather": ["main", "description","icon", "id"],
        "main": ["temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity"],
    }

weather_api_units = {   'metric': {
                            "temp": "°C",
                            "feels_like": "°C",
                            "temp_min": "°C",
                            "temp_max": "°C",
                            "pressure": "hPa",
                            "humidity": "%",
                            "visibility": "meters",
                            "speed": "m/s" ,
                            "deg": "°" ,
                            "gust":"m/s" ,
                            "1h": "mm"
                        },
                        'imperial': {
                            "temp": "°F",
                            "feels_like": "°F",
                            "temp_min": "°F",
                            "temp_max": "°F",
                            "pressure": "hPa",
                            "humidity": "%",
                            "visibility": "meters",
                            "speed": "miles/hour," ,
                            "deg": "°" ,
                            "gust":"miles/hour," ,
                            "1h": "mm"
                        }
                }
# used to replace the keys in the weather dictionary with more human-readable descriptions
weather_replace_descriptions =  [
    'Current conditions' , 'Description' , 'Now' ,
    'Feels like' , 'Low' , 'High' , 'Pressure' , 'Humidity'
    ]
############################### Managing locations and persisitent settings ####################################

def read_locations():
    """
    Reads the locations from the 'settings.json' file and returns them as a list.
    Returns:
        list: A list of locations.
    """
    locations_file = Path("./settings.json")
    if locations_file.exists() and locations_file.is_file() and locations_file.stat().st_size > 0:
        with open('./settings.json', 'r') as f:
            locations = json.load(f)
    else:
        locations = {}
    return locations

def store_locations():
    """
    Stores the locations in a JSON file.
    This function saves the locations to a JSON file named 'settings.json' in the current directory.
    It uses the 'json' module to serialize the 'locations' variable and writes it to the file.
    Args:
        None
    Returns:
        None
    """
    with open('./settings.json', 'w') as f:
        #print_locations()
        json.dump(locations, f, indent=4)


def print_locations():
    """
    Prints the locations in a human-readable format.
    This function prints the locations in a human-readable format.
    Args:
        None
    Returns:
        None
    """
    print(" print_locations: ")
    print(f"len(locations) = {len(locations)}")
    print(f"=========== Locations settings \n {json.dumps(locations, indent=4)} ")



def store_conf(parameter, value):
    """
    Stores the given parameter and its corresponding value in a configuration file.

    Args:
        parameter (str): The parameter to store.
        value: The value of the parameter.

    Returns:
        None
    """
    try:
        f = open(conf_file_name, "rb")
    except FileNotFoundError:
        print('error FileNotFoundError')
        pass
    else:
        with f:
            toml_dict = tomlkit.parse(f.read())
            if parameter not in toml_dict.keys():
                toml_dict[parameter] = value
            else:
                toml_dict[parameter] = value
            f.close()
            f = open(conf_file_name, "w")
            f.write(tomlkit.dumps(toml_dict))
            f.close()


def read_conf(parameter):
    """
    Reads the configuration file and returns the value of the specified parameter.

    Parameters:
    - parameter (str): The name of the parameter to retrieve from the configuration file.

    Returns:
    - The value of the specified parameter if found in the configuration file.
    - "UTC" if the parameter is 'timezone' and not found in the configuration file.
    - "Celcius" if the parameter is 'units' and not found in the configuration file.
    - None if the parameter is not found in the configuration file and is not 'timezone' or 'units'.
    """
    try:
        f = open(conf_file_name, "rb")
    except FileNotFoundError:
        print('error FileNotFoundError')
        pass
    else:
        with f:
            toml_dict = tomlkit.parse(f.read())
            if toml_dict is not None and toml_dict.get(parameter) is not None:
                f.close()
                return toml_dict[parameter]

    # Defaults if none found
    f.close()
    if parameter == 'timezone':
        return "UTC"
    elif parameter == 'units':
        return "Celcius"
    else:
        return None


def print_time_for_stored_timezone(print_in_place=False):
    datetime_sel_tz = datetime.now(pytz.timezone(read_conf('timezone')))
    local_time= datetime_sel_tz.strftime('%A, %B %d, %Y, %I:%M %p %Z %z')
    if print_in_place:
        print(local_time)
    return f"{local_time}"


############################### API keys ####################################
api_secret_file = "./.streamlit/secrets.toml"
def my_api_key():
    """
    Retrieves the OpenWeatherMap API key from a secret file or prompts the user to enter it.

    If a secret file containing the API key exists and is not empty, the function reads the key from the file.
    Otherwise, it prompts the user to enter the API key manually.

    Returns:
        str: The OpenWeatherMap API key.

    """
    key_file = Path(api_secret_file)
    if key_file.exists() and key_file.is_file() and key_file.stat().st_size > 0:
        with open(api_secret_file, "rb") as f:
            toml_dict = tomlkit.parse(f.read())
            return toml_dict['openweathermap_api_key']
    else:
        return input("Please enter your OpenWeatherMap API key: ")

############################### Weather parsing and respresentation  ####################################
def print_city_weather(city_name, api_key, print_in_place=False):
    """
    Prints the weather information for a given city.
    Args:
        city_name (str): The name of the city.
        api_key (str): The API key for accessing the weather data.
        print_in_place (bool, optional): Whether to print the weather information in place. Defaults to False.

    Returns:
        weather: The dictionary with weather information for the city.

    """
    status, weather = weather_checker(city_name, api_key)
    if status != True:
        weather = {}
        weather[f"Error retrieving current weather in {city_name}"] = f"Please be sure this is valid location name or try again later."

    if print_in_place:
        print(f"\nCurrent weather in {city_name.capitalize()}")
        for key, value in weather.items():
            print(f"{key}: {value}")
        print("\n")

    return weather


def parse_openweather_response(json_str):

    '''
        This function parses weather information from the JSON response.
        The parsed and filtered weather information is stored in the `weather` dictionary, which contains selected weatcher properties such as
        temperature, humidity, wind speed, etc.
        The global `locations` dictionary is also updated with the city's information, including its coordinates, timezone, and units.
    '''
    data = json.loads(json_str)
    city = data["name"]
    if city not in locations.keys():
        locations[city.lower()] = {}

    weather = {}

    units_system = weather_api_units[get_units()]
    for key, value in data.items():
        for api_key, api_value in weather_api1.items():
            if api_key  == key:
                if isinstance(value, list):
                    # As 'weather' is the only list in API response, we can take only first weather report here
                    weather_report0 = value[0]
                    for item in weather_report0.keys():
                        if item not in exclude_list and item in api_value:
                            if item in units_system.keys():
                                weather[item] = f"{weather_report0[item]} {units_system.get(item)}"
                            else:
                                weather[item] = weather_report0[item]

                elif isinstance(value, dict):
                    for item in value.keys():
                        if item not in exclude_list and item in api_value:
                            if item in units_system.keys():
                                weather[item] = f"{value[item]} {units_system.get(item)}"
                            else:
                                weather[item] = value[item]
                else:
                    if value not in exclude_list and value in api_value:
                        if value in units_system.keys():
                            weather[api_key] = f"{value}  {units_system.get(api_key)}"
                        else:
                            weather[api_key] = value
        # fix the keys in the weather dictionary to be more human-readable
        final_weather = dict(zip(weather_replace_descriptions, list(weather.values())))

        for location_key , location_value in location_settings.items()  :
            if location_key == key:
                for item in  location_settings[location_key]:
                    if isinstance(value, str) or isinstance(value, int):
                        locations[city.lower()][str(key)] = value
                    else:
                        locations[city.lower()][item] = value[item]

        if data["dt"] is not None and data["timezone"] is not None:
            local_time_at_dest = datetime.utcfromtimestamp(data["dt"]) + timedelta(seconds=data["timezone"])
            dt_at_dest_str = local_time_at_dest.strftime("%A, %B %d, %Y, %I:%M %p")
            formatted_remote_offset_hours = "{:+}".format(data["timezone"]/(60*60))
            final_weather["Time at destination"] = f"{dt_at_dest_str} UTC{formatted_remote_offset_hours}"

    return final_weather

def get_units():
    """
    Reads the units configuration from configuration file and returns the value.
    Returns:
        str: The units.
    """
    units = read_conf('units')
    if units == "Celcius":
        return "metric"
    elif units == "Fahrenheit":
        return "imperial"
    else:
        return "metric"

def weather_checker(city_name , api_key):
    '''
        The function `weather_checker(city_name)` is responsible for checking the weather information for a given city.
        It takes a `city_name` parameter as input and uses the OpenWeatherMap API to retrieve the weather data for that city.
        The function first constructs the API URL using the provided `city_name` and the API key. It then sends a GET request
        to the API and receives the response. The response is checked for any errors, and if there are no errors,
        The function calls responce parser and printer function `parse_openweather_response`
        and finally returns `True` if the weather information was successfully retrieved, and `False` otherwise.
        Overall, the `weather_checker(city_name)` function provides a convenient way to check the weather for a specific city
        using the OpenWeatherMap API.
    '''

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid={api_key}&units={get_units()}"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        print("Error: ", data["message"])
        return False  , None

    weather  = parse_openweather_response(response.text)
    store_locations()
    return True , weather