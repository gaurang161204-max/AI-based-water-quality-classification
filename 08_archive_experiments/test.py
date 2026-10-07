import matplotlib.pyplot as plt

print("Matplotlib installed successfully!")

x = ["pH", "Turbidity", "TDS", "Temperature"]
y = [7.2, 3, 350, 25]

plt.bar(x, y)
plt.title("Water Quality Parameters")
plt.xlabel("Parameters")
plt.ylabel("Values")
plt.show()