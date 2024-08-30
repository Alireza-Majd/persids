import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

# Streamlit title and description
st.title("Cell Growth and Cost Analysis")
st.write("""
This app simulates the growth of cells and calculates the associated costs over time. 
You can adjust the parameters below to see how they affect the outcomes.
""")

# Input parameters with default values
N0 = st.number_input("Initial number of cells", value=1_500_000)
Nf = st.number_input("Final number of cells after 4 days", value=3 * N0)
T = st.number_input("Time over which cells replates (days)", value=4)
initial_dishes = st.number_input("Initial number of dishes", value=3)
media_per_dish_ml = st.number_input("Media per dish (ml)", value=10)
bottle_volume_ml = st.number_input("Bottle volume (ml)", value=500)
bottle_cost = st.number_input("Cost per bottle ($)", value=150)
normocin_cost_per_ml = st.number_input("Normocin cost per ml ($)", value=284 / 20)
trypsin_cost_per_plate = st.number_input("Trypsin cost per plate ($)", value=0.124166666666667)

# Calculate cell numbers for days 31 to 50
days = np.arange(31, 51)
cell_numbers = N0 * (Nf / N0) ** ((days - 31) / T)

# Calculate the change in cell numbers day to day
daily_changes = np.diff(cell_numbers, prepend=N0)

# Calculate the number of dishes needed and media required
dishes_needed = initial_dishes * 3 ** ((days - 31) // T)
daily_media_needed = dishes_needed * media_per_dish_ml
total_media_needed = np.cumsum(daily_media_needed)

# Calculate the Normocin cost for each day
daily_normocin_cost = daily_media_needed * normocin_cost_per_ml / 1000

# Calculate the Trypsin cost for passage days (every 4th day)
daily_trypsin_cost = np.where((days - 31) % 4 == 0, dishes_needed * trypsin_cost_per_plate, 0)

# Calculate the daily cost and total cost
daily_cost = (daily_media_needed * (bottle_cost / bottle_volume_ml)) + daily_normocin_cost + daily_trypsin_cost
total_cost = np.cumsum(daily_cost)

# Create a Pandas DataFrame
data = {
    "Day": days,
    "Total Number of Cells": cell_numbers.astype(int),
    "Change from Previous Day": daily_changes.astype(int),
    "Dishes Needed": dishes_needed.astype(int),
    "Daily Media Needed (ml)": daily_media_needed.astype(int),
    "Daily Normocin Cost ($)": daily_normocin_cost.astype(float),
    "Daily Trypsin Cost ($)": daily_trypsin_cost.astype(float),
    "Daily Cost ($)": daily_cost.astype(int),
    "Media Used Until this day (ml)": total_media_needed.astype(int),
    "Total Cost ($)": total_cost.astype(float)
}

df = pd.DataFrame(data)

# Plotting the subplots in a 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# Subplot 1: Total Cost and Total Number of Cells Over Time
ax1 = axs[0, 0]
ax1.plot(df["Day"], total_cost, marker='o', linestyle='-', color='b', label='Total Cost ($)')
ax1.set_xlabel('Day')
ax1.set_ylabel('Total Cost ($)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax1.set_xticks(days)
ax1.set_xticklabels(days)
ax1.grid(True)

# Plot Total Number of Cells on the same plot with a different y-axis
ax2 = ax1.twinx()
ax2.plot(df["Day"], cell_numbers, marker='o', linestyle='-', color='g', label='Total Number of Cells')
ax2.set_ylabel('Total Number of Cells', color='g')
ax2.tick_params(axis='y', labelcolor='g')
ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax2.grid(True)

ax1.set_title('Total Cost and Total Number of Cells Over Time')

# Subplot 2: Daily Media Needed Over Time
ax3 = axs[0, 1]
sns.lineplot(x="Day", y="Daily Media Needed (ml)", data=df, ax=ax3, color="r", marker="o", label="Daily Media Needed (ml)")
ax3.set_xlabel('Day')
ax3.set_ylabel('Daily Media Needed (ml)')
ax3.set_title('Daily Media Needed Over Time')
ax3.set_xticks(days)
ax3.set_xticklabels(days)
ax3.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax3.grid(True)

# Subplot 3: Number of Dishes Needed Over Time
ax4 = axs[1, 0]
sns.lineplot(x="Day", y="Dishes Needed", data=df, ax=ax4, color="b", marker="o", label="Dishes Needed")
ax4.set_xlabel('Day')
ax4.set_ylabel('Dishes Needed')
ax4.set_title('Number of Dishes Needed Over Time')
ax4.set_xticks(days)
ax4.set_xticklabels(days)
ax4.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax4.grid(True)

# Subplot 4: Cumulative Media Use Over Time
ax5 = axs[1, 1]
sns.lineplot(x="Day", y="Media Used Until this day (ml)", data=df, ax=ax5, color="g", marker="o", label="Cumulative Media Use (ml)")
ax5.set_xlabel('Day')
ax5.set_ylabel('Cumulative Media Use (ml)')
ax5.set_title('Cumulative Media Use Over Time')
ax5.set_xticks(days)
ax5.set_xticklabels(days)
ax5.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax5.grid(True)

# Adjust the layout
plt.tight_layout()

# Show the plot in Streamlit
st.pyplot(fig)

# Save the plot as a PDF and provide a download link
plt.savefig('cell_growth_cost_analysis.pdf')
st.write("You can download the plot as a PDF:")
st.download_button(
    label="Download PDF",
    data=open('cell_growth_cost_analysis.pdf', 'rb').read(),
    file_name='cell_growth_cost_analysis.pdf',
    mime='application/pdf'
)