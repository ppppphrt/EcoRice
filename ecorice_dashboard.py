import random
import csv
from datetime import datetime
from collections import defaultdict
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


# Simulate sensor data collection with income and carbon credits
def collect_sensor_data():
    soil_moisture = random.uniform(20.0, 80.0)  # Percentage
    water_level = random.uniform(0.0, 15.0)  # cm
    air_temp = random.uniform(25.0, 35.0)  # Celsius
    air_humidity = random.uniform(40.0, 90.0)  # Percentage
    co2_emissions = random.uniform(300, 450)  # ppm
    income = round(random.uniform(100, 1000), 2)  # Simulated income in dollars
    carbon_credit = round((450 - co2_emissions) * 0.1, 2)  # Simulated carbon credits

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": soil_moisture,
        "water_level": water_level,
        "air_temp": air_temp,
        "air_humidity": air_humidity,
        "co2_emissions": co2_emissions,
        "income": income,
        "carbon_credit": carbon_credit,
    }


# Store data into a CSV file
def save_data_to_csv(data, filename="ecorice_data.csv"):
    fieldnames = ["timestamp", "soil_moisture", "water_level", "air_temp", "air_humidity", "co2_emissions", "income",
                  "carbon_credit"]
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Write headers only if the file is new
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")


# Aggregate data into a DataFrame
def load_monthly_data(filename="ecorice_data.csv"):
    try:
        data = pd.read_csv(filename)
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data["month"] = data["timestamp"].dt.to_period("M").astype(str)
        monthly_data = data.groupby("month").agg({
            "income": "mean",
            "carbon_credit": "mean"
        }).reset_index()
        return monthly_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()


# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("EcoRice Monthly Comparison", style={"text-align": "center"}),
    dcc.Graph(id="monthly-comparison-chart"),
    dcc.Interval(
        id="interval-component",
        interval=10 * 1000,  # Update every 10 seconds
        n_intervals=0
    )
])


@app.callback(
    Output("monthly-comparison-chart", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_chart(n_intervals):
    monthly_data = load_monthly_data()
    if monthly_data.empty:
        return {"data": [], "layout": {"title": "No Data Available"}}

    figure = {
        "data": [
            {
                "x": monthly_data["month"],
                "y": monthly_data["income"],
                "type": "bar",
                "name": "Average Income ($)",
            },
            {
                "x": monthly_data["month"],
                "y": monthly_data["carbon_credit"],
                "type": "bar",
                "name": "Average Carbon Credit",
            },
        ],
        "layout": {
            "title": "Monthly Income and Carbon Credit Comparison",
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Value"},
            "barmode": "group",
        },
    }
    return figure


# Simulate data collection
if __name__ == "__main__":
    print("Starting EcoRice data simulation...")
    for _ in range(10):  # Simulate 10 data entries
        data = collect_sensor_data()
        save_data_to_csv(data)
        print(f"Collected and saved data: {data}")

    print("Launching Dash app...")
    app.run_server(debug=True)
