import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_differentiation_cost(target_cells, initial_cells, doubling_time, media_cost_per_bottle, bottle_volume, max_cells_per_well, wells_per_plate, media_change_interval_days):
    total_days = 0
    current_cells = initial_cells
    cumulative_costs = []
    total_bottles_used = 0

    while current_cells < target_cells:
        total_days += doubling_time
        current_cells *= 2

        # Calculate the number of wells and plates needed
        wells_needed = np.ceil(current_cells / max_cells_per_well)
        plates_needed = np.ceil(wells_needed / wells_per_plate)
        
        # Calculate the media needed per change and how many bottles that requires
        media_needed = plates_needed * wells_per_plate * max_cells_per_well / max_cells_per_well  # 1 well per plate * max_cells_per_well
        bottles_needed = np.ceil(media_needed / bottle_volume)
        total_bottles_used += bottles_needed

        # Calculate cost at each media change interval
        cost = bottles_needed * media_cost_per_bottle if total_days % media_change_interval_days == 0 else 0
        cumulative_costs.append(cost)

    cumulative_costs = np.cumsum(cumulative_costs)
    return cumulative_costs, total_days, total_bottles_used

st.title('Differentiation Cost Calculator')
st.markdown("""
This app calculates the cost of a cell differentiation protocol based on various parameters. Adjust the inputs to see how costs accumulate.
""")

# Input widgets
target_cells = st.number_input('Target Number of Cells', value=1e6, format='%.0f')
initial_cells = st.number_input('Initial Number of Cells', value=1e4, format='%.0f')
doubling_time = st.number_input('Doubling Time (days)', value=1.5)
media_cost_per_bottle = st.number_input('Cost per Bottle of Media ($)', value=300.0, format='%.2f')
bottle_volume = st.number_input('Volume per Bottle (liters)', value=0.5, format='%.3f')
max_cells_per_well = st.number_input('Max Cells per Well', value=1e5, format='%.0f')
wells_per_plate = st.number_input('Wells per Plate', value=96, format='%.0f')
media_change_interval_days = st.number_input('Media Change Interval (days)', value=3, format='%.0f')

# Perform calculations
cumulative_costs, total_days, total_bottles_used = calculate_differentiation_cost(target_cells, initial_cells, doubling_time, media_cost_per_bottle, bottle_volume, max_cells_per_well, wells_per_plate, media_change_interval_days)

# Display results in a table
total_cost = cumulative_costs[-1] if cumulative_costs.size > 0 else 0
results_df = pd.DataFrame({
    "Metric": ["Total Cost", "Total Days", "Total Bottles Used"],
    "Value": [f"${total_cost:.2f}", int(total_days), int(total_bottles_used)]
})

st.table(results_df)

# Plotting the cumulative cost over time
fig, ax = plt.subplots()
days = np.arange(1, len(cumulative_costs) + 1) * doubling_time
ax.plot(days, cumulative_costs, marker='o', linestyle='-', color='b')
ax.set_title('Cumulative Cost Over Time')
ax.set_xlabel('Days')
ax.set_ylabel('Cumulative Cost ($)')
ax.grid(True)

st.pyplot(fig)

st.markdown("""
**Note:** Costs are calculated based on media change intervals, the number of wells required, and the doubling time of the cells.
""")