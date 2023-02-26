import datetime  # Because we need to time-travel back to fix our mistakes
import matplotlib.pyplot as plt  # For creating visual art that makes people think we're smart
import requests  # For sending love letters to the API
import mplcursors  # To magically hover over the data and make our dreams come true

api_url = "https://agsi.gie.eu/api" # The secret hideout of the gas storage data
weather_url = "https://archive-api.open-meteo.com/v1/archive" # The magical gateway to the weather data

# Determine the current date and subtract one year, because who has time to remember dates
now = datetime.datetime.now()
one_year_ago = now - datetime.timedelta(days=365)

# Parameters for the gas storage data API request, we ask nicely and hope for the best
params = {
    "country": "de",
    "from": one_year_ago.strftime("%Y-%m-%d"),
    "to": now.strftime("%Y-%m-%d"),
    "size": 365
}

# Parameters for the weather data API request, we tell the weather to come to us
weather_params = {
    "latitude": 51.20,
    "longitude": 6.47,
    "start_date": one_year_ago.strftime("%Y-%m-%d"),
    "end_date": now.strftime("%Y-%m-%d"),
    "hourly": "temperature_2m"
}

# Get the gas storage data from the API, because we love data more than anything
response = requests.get(api_url, params=params)
gas_data = [float(d["gasInStorage"]) for d in response.json()["data"]]

# Get the temperature data from the weather API and resample it to daily data, because we like things smooth
weather_response = requests.get(weather_url, params=weather_params)
temperature_data = weather_response.json()["hourly"]["temperature_2m"]
tag_temperature = []
temp_sum = 0
for i, temp in enumerate(temperature_data):
    if temp is not None:
        temp_sum += temp
    if i % 24 == 23:
        tag_temperature.append(temp_sum/24)
        temp_sum = 0

# Create a file with the current date and time as the name, because we're organized like that
filename = now.strftime("%Y-%m-%d_%H-%M-%S_data.txt")
with open(filename, "w") as file:
    for temp, gas in zip(tag_temperature, gas_data):
        file.write(f"{temp};{gas}\n")

# Create a figure with two subplots for the gas storage and temperature data, because we're fancy like that
fig, axs = plt.subplots(2, figsize=(16, 9))
fig.patch.set_facecolor('#1a1a1a') 

# Set the colors of the labels and tick marks for each axis, because details matter
axs[0].tick_params(colors='#f5f5f5')
axs[1].tick_params(colors='#f5f5f5')

# Set the colors of the grid lines, because we want them to feel included
axs[0].grid(color='#2c2c2c')
axs[1].grid(color='#2c2c2c')
axs[0].set_facecolor('#1a1a1a')
axs[1].set_facecolor('#1a1a1a')

# Set the titles and axis labels for each subplot, because we're storytellers at heart
axs[0].set_title("Gas Storage", color='red')
axs[1].set_title("Temperature", color='blue')
axs[0].set_ylabel('Gas in Twh', color="#f5f5f5") 
axs[0].set_xlabel('Days', color="#f5f5f5")  
axs[1].set_xlabel('Days', color="#f5f5f5")  
axs[1].set_ylabel('Temperature', color="#f5f5f5")  

# Plotting the gas and temperature data in style!
mplcursors.cursor(axs[0].plot(gas_data, color='red'), hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Day: {sel.target[0]}\nGas: {sel.target[1]:.2f} TWh\nTemp: {tag_temperature[int(sel.target[0])]:.2f} °C"))
mplcursors.cursor(axs[1].plot(tag_temperature, color='blue'), hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Day: {sel.target[0]}\nGas: {gas_data[int(sel.target[0])]:.2f} TWh\nTemp: {sel.target[1]:.2f} °C"))

# Time to export our amazing visualizations
plt.savefig(f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_squares1.png",
            bbox_inches="tight",
            pad_inches=1,
            edgecolor='w',
            orientation='landscape')
           
plt.show()
