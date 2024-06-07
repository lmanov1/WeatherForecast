# Weather Watchdog Application

This application allows you to monitor the weather conditions in your favorite locations all around the word. It uses the OpenWeatherMap API to retrieve and display the weather data.
Application have two versions - one on streamlit platform (available online) 
and another - as a python sript interacting via the user console. 
Details below.

## Getting Started
### Streamlit version

*There is a sidebar that allows you to navigate through the application*

First , you need to enter at least one city name (i.e. 'location') . You can do this by either choosing '**Enter city name**' option on the sidebar or via the 'manage stored locations' in '**Settings**' (see below). In both cases you can add multiple locations for continuous monitoring.
Current weather for any stored locations will be available @ '**My cities**' sidebar's menu

You can configure your preferences with the sidebar's '**Settings**' option. 
Available options in this menu currently include:
* Choosing temperature units to use (Celsius or Fahrenheit)
* Managing your stored locations (add/remove locations)   
* Updating your local timezone. This allows streamlit to correctly display your local time 😊

You can monitor weather conditions in stored locations at any time by chossing '**My cities**' option from the sidebar.

### Console Python version

To start using the application, you will be prompted to enter a city name on console. Current weather conditions at the destination are printed rigth away , and the location will be stored persistently as you preference for the future use. Each time you start anew , you will be presented with current weather in all the previously stored locations , plus a prompt to enter any other location - or quit. 
## How It Works

The application sends requests using the OpenWeatherMap's RESTful API and receives JSON responses. Those responses are checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed.

## User Preferences

Any location you enter is stored as your preference for future use. The next time you run the application, as long as you do not choose to change your preferences or add more locations, you will be presented with the current weather conditions in all stored locations.
Same apply to any other settings.

## Live Demo

You can access a live demo of the application [Here](https://weatherforecast-yhgyten7mk2jmtewukn5yy.streamlit.app/ "Weather Watchdog")

*Best seen with dark browser theme*

## Cloning and running locally 
*Please pay attention, poetry installation required in order to activate virtual environment*
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