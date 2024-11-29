# This data was gathered from the Federal Reserve at the following URL:
# https://www.federalreserve.gov/paymentsystems/2022-The-Federal-Reserve-Payments-Study-Initial-Data-accessible.htm#Figure1

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data for ACH returns by month and company
data = [
    [2000, "Checks", 40.30],
    [2003, "Checks", 40.86],
    [2006, "Checks", 41.47],
    [2009, "Checks", 34.07],
    [2012, "Checks", 27.21],
    [2015, "Checks", 29.18],
    [2018, "Checks", 26.77],
    [2021, "Checks", 27.23],
    [2000, "ACH Debits", 9.24],
    [2003, "ACH Debits", 11.87],
    [2006, "ACH Debits", 13.32],
    [2009, "ACH Debits", 15.03],
    [2012, "ACH Debits", 18.65],
    [2015, "ACH Debits", 19.60],
    [2018, "ACH Debits", 23.28],
    [2021, "ACH Debits", 33.19],
    [2000, "ACH Credits", 8.62],
    [2003, "ACH Credits", 12.23],
    [2006, "ACH Credits", 17.70],
    [2009, "ACH Credits", 22.14],
    [2012, "ACH Credits", 27.51],
    [2015, "ACH Credits", 32.48],
    [2018, "ACH Credits", 40.87],
    [2021, "ACH Credits", 58.66],
    [2000, "Credit Cards", 1.28],
    [2003, "Credit Cards", 1.68],
    [2006, "Credit Cards", 2.12],
    [2009, "Credit Cards", 1.92],
    [2012, "Credit Cards", 2.55],
    [2015, "Credit Cards", 3.05],
    [2018, "Credit Cards", 3.98],
    [2021, "Credit Cards", 4.88],
    [2000, "Non-prepaid Debit Cards", 0.35],
    [2003, "Non-prepaid Debit Cards", 0.63],
    [2006, "Non-prepaid Debit Cards", 0.97],
    [2009, "Non-prepaid Debit Cards", 1.46],
    [2012, "Non-prepaid Debit Cards", 1.87],
    [2015, "Non-prepaid Debit Cards", 2.18],
    [2018, "Non-prepaid Debit Cards", 2.75],
    [2021, "Non-prepaid Debit Cards", 3.94],
    [2000, "Prepaid Debit Cards", 0.00],
    [2003, "Prepaid Debit Cards", 0.00],
    [2006, "Prepaid Debit Cards", 0.08],
    [2009, "Prepaid Debit Cards", 0.14],
    [2012, "Prepaid Debit Cards", 0.23],
    [2015, "Prepaid Debit Cards", 0.29],
    [2018, "Prepaid Debit Cards", 0.35],
    [2021, "Prepaid Debit Cards", 0.61],
]

# Create a DataFrame
df = pd.DataFrame(data, columns=["year", "payment_type", "amount"])
df["payment_type"] = df["payment_type"].astype("category")

# Plotting the number of ACH returns by month and company with different markers
plt.figure(figsize=(14, 8))

# Define custom markers for each payment type
markers = {
    "Checks": "o",
    "ACH Debits": "s",
    "ACH Credits": "D",
    "Credit Cards": "X",
    "Non-prepaid Debit Cards": "P",
    "Prepaid Debit Cards": "H",
}

sns.lineplot(
    x="year",
    y="amount",
    hue="payment_type",
    data=df,
    style="payment_type",
    markers=markers,
)

# plt.title("Trends in Non-Cash Payments", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Trillions of Dollars", fontsize=14)
plt.xticks(ticks=range(2000, 2022, 1), rotation=45)
plt.legend(title="Payment Type")
plt.tight_layout()

# Save the plot as an SVG file
plt.savefig("trends_in_noncash_payments.svg")

# Show the plot
plt.show()
