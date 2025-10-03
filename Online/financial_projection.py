import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Set up the months for the x-axis
months = np.arange(1, 13)
month_labels = ['Month ' + str(i) for i in months]

# Define the income streams
etsy_income = [0, 100, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100]
tiktok_income = [0, 50, 150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500]
drone_income = [0, 0, 0, 0, 0, 0, 0, 500, 1000, 1500, 2000, 2500]

# Calculate the total income
total_income = [e + t + d for e, t, d in zip(etsy_income, tiktok_income, drone_income)]

# Create the stacked area chart
plt.figure(figsize=(12, 6))

# Plot the stacked areas
plt.fill_between(months, 0, etsy_income, alpha=0.7, label='Etsy Store', color='#4CAF50')
plt.fill_between(months, etsy_income, [e + t for e, t in zip(etsy_income, tiktok_income)], 
                 alpha=0.7, label='TikTok Affiliate', color='#2196F3')
plt.fill_between(months, [e + t for e, t in zip(etsy_income, tiktok_income)], total_income, 
                 alpha=0.7, label='Drone Videography', color='#9C27B0')

# Add target income range
plt.axhline(y=2000, color='r', linestyle='--', alpha=0.7, label='Target Income Range (Min)')
plt.axhline(y=5000, color='r', linestyle='--', alpha=0.7, label='Target Income Range (Max)')
plt.fill_between(months, 2000, 5000, color='r', alpha=0.1)

# Customize the chart
plt.title('12-Month Income Projection (AUD)', fontsize=16)
plt.xlabel('Timeline', fontsize=12)
plt.ylabel('Monthly Income (AUD)', fontsize=12)
plt.xticks(months, month_labels, rotation=45)
plt.grid(True, alpha=0.3)

# Format y-axis to show AUD
formatter = ticker.FormatStrFormatter('$%1.0f')
plt.gca().yaxis.set_major_formatter(formatter)

# Add legend
plt.legend(loc='upper left')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the chart
plt.savefig('financial_projection.png', dpi=300)
