# Welcome  to Weather Watchdog Application
This application is actually my Python project , and is a part of my ongoing certification as a data scientist (at BIU).   
This application allows you to monitor weather conditions in your favorite locations all around the word. It uses the OpenWeatherMap API to retrieve and display the weather data.
The application has two versions - one on streamlit WEB UI platform (link below) 
and the another - an interactive python script the should be run on user terminal.
Included notebook is deprecated , while still functional.
While terminal version is very basic , implementing only core project requirements (plus some extra like secrets management and persistent user preferences) , the Streamlit Web UI version implements the wast majority of stretch goals defined for the project.

## Getting Started
### Streamlit version

*There is a sidebar that allows you to navigate through the application*

#### First, the user needs to enter at least one city name (i.e. 'location').
The user can perform this by either choosing '**My cities**' option on the sidebar or via the '**manage stored locations**' from '**Settings**' menu on sidebar (details below).   
In both cases the user can add multiple locations for continuous monitoring.    
Up-to-date weather for any stored locations will be available since added at '**My cities**' sidebar's menu

#### The user can configure his preferences with the sidebar's '**Settings**' option.    
Available options in this menu currently include:
* Choosing temperature units (Celsius or Fahrenheit)
* Managing stored locations (add/remove locations)   
* Updating local timezone. This allows streamlit to correctly display local time 😊

#### The user can monitor weather conditions in stored locations by choosing '**My cities**' option from the sidebar.

### Console Python version
To start using the application, the user will be prompted to enter a valid OpenWeather API key , which will be encoded on base 64 and stored locally for subsequent use.
Next step - the user will be prompted to enter a city name on console. Current weather conditions at the destination are printed rigth away, and the location will be stored persistently as a preference for future use. 


Each time the user starts anew, he or she will be presented with the current weather in all the previously stored locations, and a prompt to enter any additional location - or quit the application. 
## Functional overview

The application sends requests using the OpenWeatherMap's RESTful API and receives JSON responses. Those responses are checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed , and a location is added to preferences.

## User Preferences

Any location the user enters is stored as a preference for future use. The next time the user runs the application, he or she will be presented with the current weather conditions in all the stored locations.
Stored locations are manageable in the settings.

## Live Demo

It is possible to access a live demo of the application [Here (streamlit app)](https://weatherforecast-feb83tnyvugr8huhxsvasy.streamlit.app/ "Weather Watchdog")

*Best seen with dark browser theme*

## Cloning and running locally 
*Please pay attention, poetry installation is required in order to activate a virtual environment*
```bash
    git clone git@github.com:lmanov1/WeatherForecast.git
    cd WeatherForecast
    poetry shell
    python3 main.py
```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the terms of the MIT license.