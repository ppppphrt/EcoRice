import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
from datetime import datetime
import matplotlib
from matplotlib import pyplot as plt

# Ensure Matplotlib uses TkAgg backend for external windows
matplotlib.use('TkAgg')

# Function to simulate sensor data collection
def collect_sensor_data():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": random.uniform(20.0, 80.0),  # Percentage
        "water_level": random.uniform(0.0, 15.0),  # cm
        "air_temp": random.uniform(25.0, 35.0),  # Celsius
        "air_humidity": random.uniform(40.0, 90.0),  # Percentage
        "co2_emissions": random.uniform(300, 450),  # ppm,
    }

# Function to save data to CSV
def save_data_to_csv(data, filename="ecorice_data.csv"):
    fieldnames = ["timestamp", "soil_moisture", "water_level", "air_temp", "air_humidity", "co2_emissions"]
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Write headers only if the file is new
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        messagebox.showerror("Error", f"Error writing to CSV: {e}")

# Function to update sensor data on GUI
def update_data():
    global current_data
    current_data = collect_sensor_data()
    soil_moisture_var.set(f"{current_data['soil_moisture']:.2f} %")
    water_level_var.set(f"{current_data['water_level']:.2f} cm")
    air_temp_var.set(f"{current_data['air_temp']:.2f} °C")
    air_humidity_var.set(f"{current_data['air_humidity']:.2f} %")
    co2_emissions_var.set(f"{current_data['co2_emissions']:.2f} ppm")

# Function to save current data
def save_data():
    if current_data:
        save_data_to_csv(current_data)
        messagebox.showinfo("Success", "Data saved successfully!")

# Function to plot CO2 emissions trend
def plot_co2_emissions(filename="ecorice_data.csv"):
    timestamps = []
    co2_emissions = []

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamps.append(row["timestamp"])
                co2_emissions.append(float(row["co2_emissions"]))

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, co2_emissions, marker="o", label="CO2 Emissions (ppm)")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Time")
        plt.ylabel("CO2 Emissions (ppm)")
        plt.title("CO2 Emissions Over Time")
        plt.legend()
        plt.tight_layout()
        plt.show()  # Display graph in an external window
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting data: {e}")

# Function to plot multiple historical metrics
def plot_historical_data(filename="ecorice_data.csv"):
    timestamps = []
    co2_levels = []
    water_levels = []

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamps.append(row["timestamp"])
                co2_levels.append(float(row["co2_emissions"]))
                water_levels.append(float(row["water_level"]))

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, co2_levels, marker='o', label="CO₂ Levels (ppm)")
        plt.plot(timestamps, water_levels, marker='o', label="Water Level (cm)", linestyle='--')
        plt.title("Historical Data")
        plt.xlabel("Timestamp")
        plt.ylabel("Values")
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting historical data: {e}")


# Initialize GUI
app = tk.Tk()
app.title("EcoRice Sensor Data")
app.geometry("400x400")

# Variables for displaying sensor data
soil_moisture_var = tk.StringVar()
water_level_var = tk.StringVar()
air_temp_var = tk.StringVar()
air_humidity_var = tk.StringVar()
co2_emissions_var = tk.StringVar()
current_data = {}

# UI Layout
ttk.Label(app, text="EcoRice Sensor Data", font=("Arial", 16)).pack(pady=10)

frame = ttk.Frame(app)
frame.pack(pady=10)

ttk.Label(frame, text="Soil Moisture:").grid(row=0, column=0, sticky="w")
ttk.Label(frame, textvariable=soil_moisture_var).grid(row=0, column=1, sticky="w")

ttk.Label(frame, text="Water Level:").grid(row=1, column=0, sticky="w")
ttk.Label(frame, textvariable=water_level_var).grid(row=1, column=1, sticky="w")

ttk.Label(frame, text="Air Temperature:").grid(row=2, column=0, sticky="w")
ttk.Label(frame, textvariable=air_temp_var).grid(row=2, column=1, sticky="w")

ttk.Label(frame, text="Air Humidity:").grid(row=3, column=0, sticky="w")
ttk.Label(frame, textvariable=air_humidity_var).grid(row=3, column=1, sticky="w")

ttk.Label(frame, text="CO2 Emissions:").grid(row=4, column=0, sticky="w")
ttk.Label(frame, textvariable=co2_emissions_var).grid(row=4, column=1, sticky="w")

ttk.Button(app, text="Update Data", command=update_data).pack(pady=5)
ttk.Button(app, text="Save Data", command=save_data).pack(pady=5)
ttk.Button(app, text="Plot CO2 Emissions", command=plot_co2_emissions).pack(pady=5)

ttk.Button(app, text="Plot Historical Data", command=plot_historical_data).pack(pady=5)

# Start the GUI event loop
app.mainloop()
