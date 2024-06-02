# Weather Forecast Application

This application allows you to monitor the weather conditions in your favorite locations all around the word. It uses the OpenWeatherMap API to retrieve and display the weather data.
Application have two versions - one on streamlit platform available online 
And another - a python sript interacting via the user console. 
Details below.

## Getting Started
**Streamlit version**

There is a sidebar that allows you to navigate through the application.
To start using the application, you will need to enter a city name ('**Enter city name**'). Current weather at the location (if exists) will be displayed. You also have an option to configure your preferences with '**Settings**' option, such as the units to use when displaying temperatures (Celsius or Fahrenheit) , manage previously stored locations , update your current timezone and so on.
You can also monitor weather in all the previously stored locations ('**History**')

**Console Python version**

To start using the application, you will need to enter a city name. Current weather conditions at the destination are printed rigth away , and the location will be stored persistently as you preference for hte future use. Each time you start anew , you will be presented with current weather in all the previously stored locations , plus a prompt to enter ant other location - or quit. 
## How It Works

The application sends a GET request to the OpenWeatherMap API and receives a JSON response. This response is checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed to you.

## User Preferences

Any location you enter is stored as your preference for future use. The next time you run the application, as long as you do not choose to change your preferences or add more locations, you will be presented with the current weather conditions in all stored locations.

## Live Demo

You can access a live demo of the application at the following URL:
https://weatherforecast-xzsurgh5ryfbtlskwejvkc.streamlit.app/

You can  otherwise , clone repo locally and run main.py script.
Please pay attention, poetry installation required in order to activate virtual environment
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