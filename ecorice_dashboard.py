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

# Function to update the main dashboard
def update_dashboard():
    data = get_sensor_data()
    for key, value in data.items():
        labels[key].config(text=value)
    analyze_data(data)

# Function to analyze data for insights
def analyze_data(data):
    water_level = float(data["Water Level"].split()[0])
    co2_emissions = float(data["CO₂ Emissions"].split()[0])
    insights = []
    if water_level < 7:
        insights.append("Add water to the field.")
    if co2_emissions > 400:
        insights.append("Monitor CO₂ levels.")
    if not insights:
        insights.append("All parameters are within optimal range.")
    # Display insights
    insight_text.set("\n".join(insights))

# Function to calculate carbon credits
def calculate_carbon_credits():
    co2_reduction = random.uniform(100, 300)  # Mock CO₂ reduction value
    income = co2_reduction * 0.5  # Assume 0.5 THB per kg of CO₂ reduced
    messagebox.showinfo("Carbon Credits", f"CO₂ Reduction: {co2_reduction:.2f} kg\nPotential Income: {income:.2f} THB")

# Function to calculate profit or loss
def calculate_profit_or_loss():
    try:
        cost = float(cost_var.get())
        revenue = float(revenue_var.get())
        net_profit = revenue - cost
        result_text.set(f"Net Profit: {'{:.2f}'.format(net_profit)} THB")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for cost and revenue.")

# Function to plot historical data
def plot_historical_data():
    timestamps = ["10:00", "11:00", "12:00", "13:00", "14:00"]
    co2_levels = [400, 390, 420, 410, 380]  # Mock data
    water_levels = [10, 9, 8, 7.5, 7]  # Mock data

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, co2_levels, marker='o', label="CO₂ Levels (ppm)")
    plt.plot(timestamps, water_levels, marker='o', label="Water Level (cm)", linestyle='--')
    plt.title("Historical Data")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.legend()
    plt.grid()
    plt.show()

# Function to switch pages
def switch_frame(frame):
    frame.tkraise()

# Initialize the main Tkinter app
app = tk.Tk()
app.title("EcoRice Dashboard")
app.geometry("500x700")
app.resizable(False, False)

# Create Frames for Pages
dashboard_frame = ttk.Frame(app)
insight_frame = ttk.Frame(app)
graph_frame = ttk.Frame(app)
account_frame = ttk.Frame(app)

for frame in (dashboard_frame, insight_frame, graph_frame, account_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# ------------------------------
# Dashboard Page
# ------------------------------
ttk.Label(dashboard_frame, text="EcoRice Dashboard", font=("Arial", 24)).pack(pady=20, anchor="center")

frame = ttk.Frame(dashboard_frame)
frame.pack(pady=10)

labels = {}
for param in ["Soil Moisture", "Water Level", "Temperature", "Humidity", "CO₂ Emissions"]:
    row_frame = ttk.Frame(frame)
    row_frame.pack(fill="x", pady=5)
    ttk.Label(row_frame, text=f"{param}:", font=("Arial", 14), width=20, anchor="e").pack(side="left", padx=5)
    labels[param] = ttk.Label(row_frame, text="N/A", font=("Arial", 14, "bold"), foreground="green", anchor="w")
    labels[param].pack(side="left")

# Centered button frame
button_frame = ttk.Frame(dashboard_frame)
button_frame.pack(pady=30)

ttk.Button(button_frame, text="Update Data", command=update_dashboard, width=25).pack(pady=5 ,padx=100)
ttk.Button(button_frame, text="Calculate Carbon Credits", command=calculate_carbon_credits, width=25).pack(pady=5)
ttk.Button(button_frame, text="Go to Insights", command=lambda: switch_frame(insight_frame), width=25).pack(pady=5)
# ttk.Button(button_frame, text="Go to Graphs", command=lambda: switch_frame(graph_frame), width=25).pack(pady=5)
ttk.Button(button_frame, text="Go to Household Account", command=lambda: switch_frame(account_frame), width=25).pack(pady=5)

# ------------------------------
# Insights Page
# ------------------------------
ttk.Label(insight_frame, text="Insights", font=("Arial", 24)).pack(pady=20, anchor="center")

insight_text = tk.StringVar()
insight_label = ttk.Label(insight_frame, textvariable=insight_text, font=("Arial", 14), wraplength=400, foreground="blue", anchor="center")
insight_label.pack(pady=20)

ttk.Button(insight_frame, text="Back to Dashboard", command=lambda: switch_frame(dashboard_frame), width=25).pack(pady=10)

# ------------------------------
# Graph Page
# ------------------------------
ttk.Label(graph_frame, text="Graphs", font=("Arial", 24)).pack(pady=20, anchor="center")

# ttk.Button(graph_frame, text="View Historical Data", command=plot_historical_data, width=25).pack(pady=10)
ttk.Button(graph_frame, text="Back to Dashboard", command=lambda: switch_frame(dashboard_frame), width=25).pack(pady=10)

# ------------------------------
# Household Account Page
# ------------------------------
ttk.Label(account_frame, text="Household Account", font=("Arial", 24)).pack(pady=20, anchor="center")

account_form = ttk.Frame(account_frame)
account_form.pack(pady=20)

ttk.Label(account_form, text="Total Cost (THB):", font=("Arial", 14)).grid(row=0, column=0, pady=5, padx=5, sticky="e")
cost_var = tk.StringVar()
ttk.Entry(account_form, textvariable=cost_var, width=20).grid(row=0, column=1, pady=5, padx=5)

ttk.Label(account_form, text="Total Revenue (THB):", font=("Arial", 14)).grid(row=1, column=0, pady=5, padx=5, sticky="e")
revenue_var = tk.StringVar()
ttk.Entry(account_form, textvariable=revenue_var, width=20).grid(row=1, column=1, pady=5, padx=5)

result_text = tk.StringVar(value="Net Profit: N/A")
result_label = ttk.Label(account_frame, textvariable=result_text, font=("Arial", 14, "bold"))
result_label.pack(pady=10)

ttk.Button(account_frame, text="Calculate Profit/Loss", command=calculate_profit_or_loss, width=25).pack(pady=10)
ttk.Button(account_frame, text="Back to Dashboard", command=lambda: switch_frame(dashboard_frame), width=25).pack(pady=10)

# Start with Dashboard Frame
switch_frame(dashboard_frame)

# Start the Tkinter event loop
app.mainloop()
