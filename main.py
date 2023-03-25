import aiohttp  # For sending love letters to the API
import asyncio  # For when we want our program to procrastinate as much as we do
import csv  # For saving data to a file, because we never know when we'll need it again
import datetime  # Because we need to time-travel back to fix our mistakes
import matplotlib.pyplot as plt  # For creating visual art that makes people think we're smart
import mplcursors  # To magically hover over the data and make our dreams come true
import numpy as np  # For when we need some extra math skills beyond what our fingers can count

api_url = "https://agsi.gie.eu/api"  # The secret lair of the gas storage data
weather_url = "https://archive-api.open-meteo.com/v1/archive"  # The magical portal to the weather data

# Let's go back in time 7 days, because a week is more than enough for us to make sense of the data
start = datetime.datetime.now() - datetime.timedelta(days=7)
# And back even further to the year 2009, because why not
end = start - datetime.timedelta(days=4465)

# Parameters for the gas storage data API request, let's hope the API is in a good mood today
params = {
    "country": "de",
    "from": end.strftime("%Y-%m-%d"),
    "to": start.strftime("%Y-%m-%d"),
    "size": 4465
}

# Parameters for the weather data API request, let's be polite and ask nicely
weather_params = {
    "latitude": 51.20,
    "longitude": 6.47,
    "start_date": end.strftime("%Y-%m-%d"),
    "end_date": start.strftime("%Y-%m-%d"),
    'daily': 'temperature_2m_mean',
    'timezone': 'Europe/Berlin',
}

# Get the gas storage data asynchronously, because we like to multi-task
async def get_gas_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            data = await response.json()
            return data["data"]

# Get the temperature data asynchronously, because we don't like to wait
async def get_temperature_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url, params=weather_params) as response:
            data = await response.json()
            return data["daily"]["temperature_2m_mean"]

# Let's run the async functions and wait for them to finish, because we're patient
loop = asyncio.get_event_loop()
gas_data = loop.run_until_complete(get_gas_data())
temperature_data = loop.run_until_complete(get_temperature_data())

# Unzip the gas data to get separate arrays for dates and gas values, because we're organized like that
gas_dateArray, gas_valueArray = zip(*[(d['gasDayStart'], d['gasInStorage']) for d in reversed(gas_data)])

# Save the data to a CSV file, because we like to have a backup plan
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "gas", "temperature"])
    for i in range(len(gas_dateArray)):
        writer.writerow([gas_dateArray[i], gas_valueArray[i], temperature_data[i]])

# Create a figure with two subplots for the gas storage and temperature data, because we're fancy like that
plt.style.use('dark_background')
fig, axs = plt.subplots(2, figsize=(16, 9))

# Set the colors of the grid lines, because we want them to feel included
axs[0].grid(color='white', alpha=0.3)
axs[1].grid(color='white', alpha=0.3)

# Set the titles and axis labels for each subplot, because we're storytellers at heart
axs[0].set_title("Gas Storage", color='red')
axs[1].set_title("Temperature", color='blue')
axs[0].set_ylabel('Gas in Twh', color="#f5f5f5")
axs[0].set_xlabel('Days', color="#f5f5f5")
axs[1].set_xlabel('Days', color="#f5f5f5")
axs[1].set_ylabel('Temperature', color="#f5f5f5")

gas_yAxis = np.array([float(numeric_string) for numeric_string in gas_valueArray])

# Plotting the gas and temperature data in style!
mplcursors.cursor(axs[0].plot(gas_yAxis, color='red'), hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Day: {sel.target[0]}\nGas: {sel.target[1]:.2f} TWh\nTemp: {temperature_data[int(sel.target[0])]:.2f} °C"))
mplcursors.cursor(axs[1].plot(temperature_data, color='blue'), hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Day: {sel.target[0]}\nGas: {gas_yAxis[int(sel.target[0])]:.2f} TWh\nTemp: {sel.target[1]:.2f} °C"))

plt.show()