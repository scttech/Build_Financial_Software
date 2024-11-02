import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data for payroll by month
data = {
    "Month": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "Payroll": [5000, 5200, 4800, 5100, 5300, 5500, 5700, 5900, 6000, 6200, 6100, 6300],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Plotting the payroll by month with a single color for bars
plt.figure(figsize=(10, 6))
barplot = sns.barplot(
    x="Month", y="Payroll", data=df, color="blue"
)  # You can change 'blue' to any color you prefer
plt.title("Payroll by Month Over the Year")
plt.xlabel("Month")
plt.ylabel("Payroll ($)")
plt.xticks(rotation=45)
plt.tight_layout()

# Adding value annotations on the bars
for index, row in df.iterrows():
    barplot.text(
        index, row["Payroll"] + 100, f"${row['Payroll']}", color="black", ha="center"
    )

# Show the plot
plt.show()
