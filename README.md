# Welcome to the Weather Watchdog Application
This application is my Python project and is a part of my ongoing certification as a data scientist at BIU.   
The application allows you to monitor weather conditions in your favorite locations all around the world. It uses the OpenWeatherMap API to retrieve and display the weather data.   
The application has two versions - one running on the Streamlit WEB UI platform  [link to live demo online](#live-demo)
and the other - is an interactive python script that should be run on the user's terminal.
The included notebook is deprecated, while still functional.   
While the terminal version is very basic, implementing only core project requirements (plus some extras like secrets management and persistent user preferences), the Streamlit Web UI version implements the vast majority of stretch goals defined for the project.

## Getting Started
### Streamlit version

*There is a sidebar that allows you to navigate through the application*

#### First, the user needs to enter at least one city name (i.e., 'location').
The user can perform this by either choosing the '**My cities**' option on the sidebar or via the '**Manage stored locations**' from the '**Settings**' menu on the sidebar (details below).   
In both cases, the user can add multiple locations for continuous monitoring.    
Once added, up-to-date weather reports for any stored locations are always available with the '**My cities**' option on the sidebar

#### The user can configure his preferences with the sidebar's '**Settings**' option.    
Available options in this menu currently include:
* Choosing temperature units (Celsius or Fahrenheit)
* Managing stored locations (Add/remove multiple locations)   
* Updating local timezone. This allows Streamlit to correctly display user's local time😊



### Console Python version
To start using the application, the user will be prompted to enter a valid OpenWeather API key, which will be encoded in base 64 and stored locally for subsequent use.
Next, the user will be prompted to enter a city name on the console. Current weather conditions at the destination are printed right away, and the location will be stored persistently as a preference for future use. 

Each time the user starts anew, he or she will be presented with the current weather in all the previously stored locations, and a prompt to enter any additional location - or quit the application. 

## Functional Overview

The application sends requests using the OpenWeatherMap's RESTful API and receives JSON responses. Those responses are checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed, and a location is added to preferences.   
The application provides a feature that allows you to view the current temperature in either Celsius (°C) or Fahrenheit (°F). Simply toggle between two units in the settings and get real-time weather updates in the format you prefer.   
In addition, the application's Streamlit version provides relevant graphics and an interactive map for each location.   

## User Locations Preferences

Any location the user enters is stored as a preference for future use. The next time the user runs the application, he or she will be presented with the current weather conditions in all the stored locations.

## Live Demo

It is possible to access a live demo of the application [Streamlit app here](https://weatherforecast-guhya2ufeugzbk9fugn6y6.streamlit.app/ "Weather Watchdog")

*Best seen with a dark browser theme*

## Cloning and running locally 
*Please pay attention, a poetry installation is required to activate a virtual environment*
```bash
    git clone git@github.com:lmanov1/WeatherForecast.git
    cd WeatherForecast
    poetry shell
```
Running terminal version locally
```bash
    python3 ./main.py

```
Running streamlit version locally
```bash
    streamlit run ./streamlit_app.py
