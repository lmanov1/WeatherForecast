# WeatherForecast

This is a Python project that provides a weather forecast for a given location(s) using the OpenWeatherMap API.

## Installation 
You have quite a few options to run this project, either running a pure python implementation in `main.py` or an included Juniper notebook `WeatherForecast.ipynb`.


## Running the python implementation locally
To run a python script , you need to have Python installed on your machine. You can download Python from the official website: https://www.python.org/downloads/

Once you have Python installed, you can clone this repository to your local machine using the following command

```bash
git clone git@github.com:lmanov1/WeatherForecast.git
cd WeatherForecast
```
You can now run the command below and follow interactive choices provided by application

```bash
poetry shell
python3 main.py
```

## Running the Notebook
You can run it locally from you installed Juniper environment or use one of the online resources like Google colaboratory.

### Run notebook Locally
To run the `WeatherForecast.ipynb` notebook locally on your environement, you need to have Jupyter Notebook installed on your machine.

If you choose to run a notebook locally , but don't have Juniper installed, you can install it using pip prior to running WeatherForecast.ipynb:

```bash
pip install notebook
```
Once Jupyter Notebook is installed, navigate to the directory containing the WeatherForecast.ipynb file in your terminal and run the following command:

```bash
jupyter notebook
```
This will start the Jupyter Notebook server and open your default web browser. You can then navigate to the WeatherForecast.ipynb file in the Jupyter Notebook interface and open it.

### Run notebook online 
Other option will be to open the notebook in Google colaboratory or alike enviromenment and run from there.
You can do it by typing in your browser the follow URL:
https://githubtocolab.com/lmanov1/WeatherForecast/blob/main/WeatherForecast.ipynb

Once page was opened  , choose 'Connect'(to the Google compute backend engine) , and then 'Run all' from the 'Run' menu.
Choose 'Run anyway' if warned about running a notebook which is not being authored by Google.

### A few words about running notebooks
To run the code in the notebook, you can either click on the 'Run' button at the top of the interface or use the shortcut 'Shift + Enter'. This will run the code in the currently selected cell and then select the next cell. You can run all cells in the notebook by clicking on 'Cell' -> 'Run All' in the menu.


## Run streamlit application from share.streamlit.io
https://weatherforecast-khftt8pnxtbzbd9smuuwpw.streamlit.app/


# Application logics and UI
As you run application for the first time , you will be required to enter a weather location (city name) to monitor.
You will also be prompted to configure your preferences such as units to use when displaying temperatures (Celsius/Fahrenheit).

Application uses the OpenWeatherMap Restful API to retrieve the weather data for that city .

An application sends a GET request to the API and receives the response. The response is checked for any errors, and if there are no errors, the weather information is parsed from the JSON response and displayed to you.

The location you entered stored as your preference for the next time you will run this weather checker application.

So the next time you run , as long as you do not choose an option of changing your preferences or adding more locations for monitoring ,  you will be presented with the current weather conditions in the all stored location.

