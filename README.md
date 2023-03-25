# Gas and Temperature Tracker

This is a fun little project that tracks daily gas levels and temperatures over the course of a year. Perfect for anyone who loves to monitor their bodily functions (we won't judge).


## Usage

When you run the program, it will retrieve gas storage and temperature data for a specific location and time range, save the data to a CSV file called data.csv, and create a plot to visualize the data. The plot will be displayed in a new window and will include two subplots, one for gas storage data and another for temperature data. You can hover over the data points to view annotations that show the date, gas storage value, and temperature value for each point.

## To be added

The next step is to develop an AI model using LightGBM that predicts how gas reserves in Germany will develop based on temperature. This will involve preprocessing the data, training the model, and evaluating its performance. Once the model is trained, we can use it to make predictions for future gas storage levels based on expected temperatures.

We'll also update the visualization to include predictions from the AI model and compare them to the actual gas storage levels. This will give us a better understanding of how well the model is performing and whether it can be used to make accurate predictions.

## Installation

You'll need Python and a few libraries installed to run this project. Don't worry, it's super easy! Just follow these steps:

1.  Clone this repository to your local machine.
2.  Install the required libraries by running `pip install -r requirements.txt` in your terminal.
3.  Run the script with `python main.py`.

And that's it! You're all set to track your gas and temperature like a pro.

## Contributions

We welcome contributions to this project! If you have any ideas for improving the code, adding new features, or just want to say hi, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://github.com/Coniass/python-gas_temp/blob/main/LICENSE.md). Do whatever you want with it (except claim it as your own, that's just rude).
