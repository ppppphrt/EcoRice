import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt

# Mock data function for sensor readings
def get_sensor_data():
    return {
        "Soil Moisture": f"{random.uniform(20, 80):.2f} %",
        "Water Level": f"{random.uniform(5, 15):.2f} cm",
        "Temperature": f"{random.uniform(25, 35):.2f} °C",
        "Humidity": f"{random.uniform(40, 90):.2f} %",
        "CO₂ Emissions": f"{random.uniform(300, 450):.2f} ppm"
    }

# Function to update dashboard with mock data
def update_dashboard():
    data = get_sensor_data()
    for key, value in data.items():
        labels[key].config(text=value)
    analyze_data(data)

# Function to provide insights based on mock data
def analyze_data(data):
    water_level = float(data["Water Level"].split()[0])
    co2_emissions = float(data["CO₂ Emissions"].split()[0])
    if water_level < 7:
        insight_label.config(text="Recommendation: Add water to the field.")
    elif co2_emissions > 400:
        insight_label.config(text="Recommendation: Monitor CO₂ levels.")
    else:
        insight_label.config(text="All parameters are within optimal range.")

# Function to calculate carbon credits
def calculate_carbon_credits():
    co2_reduction = random.uniform(100, 300)  # Mock CO₂ reduction value
    income = co2_reduction * 0.5  # Assume 0.5 THB per kg of CO₂ reduced
    messagebox.showinfo("Carbon Credits", f"CO₂ Reduction: {co2_reduction:.2f} kg\nPotential Income: {income:.2f} THB")

# Function to plot historical data
def plot_historical_data():
    timestamps = ["10:00", "11:00", "12:00", "13:00", "14:00"]
    co2_levels = [400, 390, 420, 410, 380]  # Mock data
    plt.plot(timestamps, co2_levels, marker='o', label="CO₂ Levels (ppm)")
    plt.title("CO₂ Levels Over Time")
    plt.xlabel("Time")
    plt.ylabel("CO₂ Levels (ppm)")
    plt.legend()
    plt.grid()
    plt.show()

# Initialize the main Tkinter app
app = tk.Tk()
app.title("EcoRice Dashboard")
app.geometry("400x600")
app.resizable(False, False)

# Header
ttk.Label(app, text="EcoRice Dashboard", font=("Arial", 20)).pack(pady=10)

# Real-Time Data Dashboard
frame = ttk.Frame(app)
frame.pack(pady=10, fill="x")

labels = {}
for param in ["Soil Moisture", "Water Level", "Temperature", "Humidity", "CO₂ Emissions"]:
    ttk.Label(frame, text=f"{param}:", font=("Arial", 12)).pack(anchor="w")
    labels[param] = ttk.Label(frame, text="N/A", font=("Arial", 12, "bold"), foreground="green")
    labels[param].pack(anchor="w")

# Insights Section
insight_label = ttk.Label(app, text="Loading insights...", font=("Arial", 12), foreground="blue", wraplength=350)
insight_label.pack(pady=10)

# Buttons for Actions
ttk.Button(app, text="Update Data", command=update_dashboard).pack(pady=5)
ttk.Button(app, text="Calculate Carbon Credits", command=calculate_carbon_credits).pack(pady=5)
ttk.Button(app, text="View Historical Data", command=plot_historical_data).pack(pady=5)

# Footer
ttk.Label(app, text="Developed for Farmers", font=("Arial", 10), foreground="gray").pack(side="bottom", pady=10)

# Initial data load
update_dashboard()

# Start the Tkinter event loop
app.mainloop()
