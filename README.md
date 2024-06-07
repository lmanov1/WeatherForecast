# Weather Watchdog Application

This application allows you to monitor weather conditions in your favorite locations all around the word. It uses the OpenWeatherMap API to retrieve and display the weather data.
The application has two versions - one on streamlit platform (available online) 
and another - as an interactive python script via the user terminal.   
Included notebook is deprecated.

## Getting Started
### Streamlit version

*There is a sidebar that allows you to navigate through the application*

#### First, the user needs to enter at least one city name (i.e. 'location').
The user can perform this by either choosing '**Enter city name**' option on the sidebar or via the '**manage stored locations**' from '**Settings**' menu on sidebar (details below).   
In both cases the user can add multiple locations for continuous monitoring.    
Up-to-date weather for any stored locations will be available @ '**My cities**' sidebar's menu

#### The user can configure your preferences with the sidebar's '**Settings**' option.    
Available options in this menu currently include:
* Choosing temperature units (Celsius or Fahrenheit)
* Managing stored locations (add/remove locations)   
* Updating local timezone. This allows streamlit to correctly display local time 😊

#### The user can monitor weather conditions in stored locations by choosing '**My cities**' option from the sidebar.

### Console Python version

To start using the application, the user will be prompted to enter a city name on console. Current weather conditions at the destination are printed rigth away, and the location will be stored persistently as a preference for future use. Each time the user starts anew, it will be presented with current weather in all the previously stored locations, and a prompt to enter an additional location - or quit the application. 
## Functional overview

The application sends requests using the OpenWeatherMap's RESTful API and receives JSON responses. Those responses are checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed , and a location is added to preferences.

## User Preferences

Any location the user enters is stored as a preference for future use. The next time the user runs the application, it will be presented with the current weather conditions in all the stored locations.
Stored locations are manageable in the settings.

## Live Demo

It is possible to access a live demo of the application [Here (streamlit app)](https://weatherforecast-bfegqddtv7ftqphrzzq84d.streamlit.app/ "Weather Watchdog")

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