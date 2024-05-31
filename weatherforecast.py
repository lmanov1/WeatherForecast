# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime
import pytz

############################### Global definitions ####################################
#exclude_list = ["icon", "id"]
global_settings = {"units":"metric"} # later take from settings !!!!
locations = {}

location_settings = { 
    "coord":["lon","lat"],    
    "sys": ["type", "id", "country", "sunrise", "sunset"],
    "timezone": "timezone"    
}

# TBD: display icon from url : https://openweathermap.org/img/wn/{icon}}@2x.png
# TBD : display timestamp , timezone , sunrise and sunset in human readable format
# TBD: weather_api  should be used to filter printed details on weather information
weather_api = ["weather", "main", "visibility", "wind", "clouds", "rain", "snow"] 

weather_api_units = { "main": 
                        {
                            "temp": "°C", 
                            "feels_like": "°C", 
                            "temp_min": "°C", 
                            "temp_max": "°C", 
                            "pressure": "hPa", 
                            "humidity": "%"
                        },                      
                     "visibility": "meters", 
                     "wind": {"speed": "m/s" , "deg": "°" , "gust":"m/s" }, 
                     "rain": {"1h": "mm"}, 
                     "snow": {"1h": "mm"}
                     }
weather = {}

############################### Locations and persisitent settings ####################################
from pathlib import Path
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
        json.dump(locations, f, indent=4)  


def print_locations(locations):
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
                      
############################### API keys #################################### 
def my_api_key():
    """
    Reads the API key from the '.security.json' file and returns it.
    Returns:
        str: The API key.
    """
    import sys
    if sys.version_info >= (3, 11):
        import tomllib
        #print("ython 3.11 or later detected, using tomllib")
    else:
        import tomli as tomllib

    key_file = Path("./.streamlit/secrets.toml")
    if key_file.exists() and key_file.is_file() and key_file.stat().st_size > 0:
        with open("./.streamlit/secrets.toml", "rb") as f:
            toml_dict = tomllib.load(f)                     
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
        str: The weather information for the city.

    """
    answer = ""     
    status, weather, remote_utc_timestamp, remote_tz_shift_secs = weather_checker(city_name, api_key)    
    if status:
        answer += f"=========== Weather in {city_name.title()} ================\n"
        answer += print_weather_with_units(weather, weather_api_units, remote_utc_timestamp=remote_utc_timestamp, remote_tz_shift_secs=remote_tz_shift_secs) 
    else:
        answer += f"Error retrieving current weather in {city_name}. Please be sure this is valid location name or try again later."        

    if print_in_place:  
        print(answer)

    return answer


def print_weather_with_units(weather_dict, units_dict, 
                             remote_utc_timestamp=None, 
                             datetime_print_format="%A, %B %d, %Y, %I:%M %p", 
                             remote_tz_shift_secs=None):
    """
    Prints the weather information with units.

    Args:
        weather_dict (dict): A dictionary containing the weather information.
        units_dict (dict): A dictionary containing the units for each weather parameter.
        remote_utc_timestamp (int, optional): The remote UTC timestamp. Defaults to None.
        datetime_print_format (str, optional): The format for printing the datetime. Defaults to "%A, %B %d, %Y, %I:%M %p".
        remote_tz_shift_secs (int, optional): The shift in seconds for the remote timezone. Defaults to None.

    Returns:
        str: The formatted weather information with relevant units.
    """
    
    answer = ""
    if remote_utc_timestamp is not None:
        # TBD : use pytz to get timezone name and use it to convert timestamp to local time
        dt_at_dest = datetime.fromtimestamp(remote_utc_timestamp)
        answer += f"Local time at destination: {dt_at_dest.strftime(datetime_print_format)}\n"
        answer += f"Timezone at destination: UTC+{(remote_tz_shift_secs/(60*60))}\n"
        
    for key, value in weather_dict.items():
        if isinstance(value, dict):
            answer += f"{key}:"
            answer += print_weather_with_units(value, units_dict.get(key, {}))
        else:
            unit = units_dict.get(key, "")
            answer += f"{key}: {value} {unit}\n"            
            
    return answer

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
        
    for key, value in data.items():        
        
        for weather_key in weather_api:
            if weather_key  == key:
                if isinstance(value, list):                                                                    
                    weather[weather_key] = value[0] # only first weather report
                else:
                    weather[weather_key] = value            

        for location_key , location_value in location_settings.items()  :
            if location_key == key:                      
                for item in  location_settings[location_key]:                                        
                    if isinstance(value, str) or isinstance(value, int):
                        locations[city.lower()][str(key)] = value
                    else:                        
                        locations[city.lower()][item] = value[item]
       
    return weather , data["dt"] , data["timezone"]    


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
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid={api_key}&units=metric"
    response = requests.get(url)    
    data = response.json()    
    if data["cod"] != 200:
        print("Error: ", data["message"])
        return False  , None , None , None
    
    store_locations()
    
    weather , remote_utc_timestamp , remote_tz_shift_secs = parse_openweather_response(response.text)
    
    return True , weather , remote_utc_timestamp , remote_tz_shift_secs