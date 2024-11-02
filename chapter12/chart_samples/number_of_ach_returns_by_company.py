import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data for ACH returns by month and company
data = [
    ["January", "Elemental Resources", 50],
    ["February", "Elemental Resources", 80],
    ["March", "Elemental Resources", 60],
    ["April", "Elemental Resources", 70],
    ["May", "Elemental Resources", 40],
    ["June", "Elemental Resources", 90],
    ["July", "Elemental Resources", 100],
    ["August", "Elemental Resources", 80],
    ["September", "Elemental Resources", 70],
    ["October", "Elemental Resources", 50],
    ["November", "Elemental Resources", 60],
    ["December", "Elemental Resources", 90],
    ["January", "Petro Power LLC", 30],
    ["February", "Petro Power LLC", 40],
    ["March", "Petro Power LLC", 50],
    ["April", "Petro Power LLC", 70],
    ["May", "Petro Power LLC", 80],
    ["June", "Petro Power LLC", 90],
    ["July", "Petro Power LLC", 100],
    ["August", "Petro Power LLC", 80],
    ["September", "Petro Power LLC", 60],
    ["October", "Petro Power LLC", 70],
    ["November", "Petro Power LLC", 50],
    ["December", "Petro Power LLC", 80],
    ["January", "Titan Industries", 60],
    ["February", "Titan Industries", 70],
    ["March", "Titan Industries", 80],
    ["April", "Titan Industries", 50],
    ["May", "Titan Industries", 60],
    ["June", "Titan Industries", 70],
    ["July", "Titan Industries", 80],
    ["August", "Titan Industries", 90],
    ["September", "Titan Industries", 60],
    ["October", "Titan Industries", 50],
    ["November", "Titan Industries", 70],
    ["December", "Titan Industries", 80],
    ["January", "Secure Finance Group", 40],
    ["February", "Secure Finance Group", 50],
    ["March", "Secure Finance Group", 60],
    ["April", "Secure Finance Group", 70],
    ["May", "Secure Finance Group", 80],
    ["June", "Secure Finance Group", 90],
    ["July", "Secure Finance Group", 70],
    ["August", "Secure Finance Group", 50],
    ["September", "Secure Finance Group", 60],
    ["October", "Secure Finance Group", 70],
    ["November", "Secure Finance Group", 80],
    ["December", "Secure Finance Group", 60],
]

# Create a DataFrame
df = pd.DataFrame(data, columns=["Month", "Company", "ACH_Returns"])
df["Company"] = df["Company"].astype("category")

# Plotting the number of ACH returns by month and company with different markers
plt.figure(figsize=(14, 8))

# Define custom markers for each company
markers = {
    "Elemental Resources": "o",
    "Petro Power LLC": "s",
    "Titan Industries": "D",
    "Secure Finance Group": "X",
}

sns.lineplot(
    x="Month",
    y="ACH_Returns",
    hue="Company",
    data=df,
    style="Company",
    markers=markers,
)

plt.title("Number of ACH Returns by Month for Different Companies")
plt.xlabel("Month")
plt.ylabel("Number of ACH Returns")
plt.xticks(rotation=45)
plt.legend(title="Company")
plt.tight_layout()

# Show the plot
plt.show()
