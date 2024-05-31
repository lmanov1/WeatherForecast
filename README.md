# Weather Forecast Application

This application allows you to monitor the weather conditions in your chosen locations. It uses the OpenWeatherMap API to retrieve and display the weather data.

## Getting Started

To start using the application, you will need to enter a city name. You will also be prompted to configure your preferences, such as the units to use when displaying temperatures (Celsius or Fahrenheit).

## How It Works

The application sends a GET request to the OpenWeatherMap API and receives a JSON response. This response is checked for errors. If there are no errors, the weather information is parsed from the JSON response and displayed to you.

## User Preferences

The location you enter is stored as your preference for future use. The next time you run the application, as long as you do not choose to change your preferences or add more locations, you will be presented with the current weather conditions in all stored locations.

## Live Demo

You can access a live demo of the application at the following URL: https://weatherforecast-axhfocads2nic84dwvjpyi.streamlit.app/

Or clone repo locally and run main.py
Please pay attention, poetry installation required in order to run project' virtual environment
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