from weatherforecast import *

api_key = my_api_key()
locations = read_locations()
print_time_for_stored_timezone( print_in_place=True )
print(f"Checking weather for stored locations:")
for location in locations:
   print_city_weather(location, api_key, print_in_place=True)

answer = input("Would you like to check another city? (yes/no)")   
if answer.lower() == "yes" or answer.lower() == "y":    
    while True:
        city = input("Enter a city name (or 'exit' to quit): ")
        if city.lower() == "exit" or city.lower() == "quit":
            store_locations()
            break
        else:        
            if len(city) == 0:            
                print("Please enter a valid city name")
                continue
            else:
                print_city_weather(city, api_key, print_in_place=True)                
                continue
else:
    store_locations()
    print("Assuming 'no' .. Exiting...")


