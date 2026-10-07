import time
import random
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load trained Random Forest model
model = joblib.load("water_model.pkl")

# Store live values for graph
samples = []
ph_values = []
turbidity_values = []
predictions = []

plt.ion()

fig, ax = plt.subplots()

print("LIVE WATER QUALITY MONITORING")
print("Press Ctrl+C to stop\n")

sample_number = 0

try:
    while True:

        sample_number += 1

        # Generate LIVE sensor-like data
        ph = round(random.uniform(5.0, 8.0), 2)
        turbidity = round(random.uniform(1.0, 25.0), 2)
        temperature = round(random.uniform(23.0, 32.0), 2)
        tds = round(random.uniform(200, 900), 2)
        conductivity = round(random.uniform(300, 1200), 2)

        # Put live data into DataFrame
        live_data = pd.DataFrame([{
            "pH": ph,
            "Turbidity": turbidity,
            "Temperature": temperature,
            "TDS": tds,
            "Conductivity": conductivity
        }])

        # Random Forest prediction
        result = model.predict(live_data)[0]

        # Store data
        samples.append(sample_number)
        ph_values.append(ph)
        turbidity_values.append(turbidity)
        predictions.append(result)

        # Terminal output
        print("--------------------------------")
        print("Sample:", sample_number)
        print("pH:", ph)
        print("Turbidity:", turbidity, "NTU")
        print("Temperature:", temperature, "°C")
        print("TDS:", tds, "ppm")
        print("Conductivity:", conductivity)
        print("AI OUTPUT:", result)

        # Update graph
        ax.clear()
        ax.plot(samples, ph_values, marker="o")

        ax.set_title("LIVE Water Quality - pH")
        ax.set_xlabel("Sample")
        ax.set_ylabel("pH")
        ax.grid(True)

        plt.pause(0.1)

        # New data every 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("\nLive monitoring stopped.")

plt.ioff()
plt.show()