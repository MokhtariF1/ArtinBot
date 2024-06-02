import fastf1 as ff1
from fastf1.core import Laps
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import seaborn as sns
import time
def top_speed(year, gp, identifier):
    race = ff1.get_event(year, gp)
    session = race.get_session(identifier)  # Use 'Q' for Qualifying, 'R' for Race, etc.
    session.load()
    top_speed_path = f"{year}-{gp}-{identifier}-top_speed.png"
    speed_trap_path = f"{year}-{gp}-{identifier}-speed_trap.png"
    # 3. Data Cleaning and Preparation
    # Extract top speed and speed trap data
    drivers = session.drivers
    driver_data = []

    for drv in drivers:
        laps = session.laps.pick_driver(drv)
        top_speed = laps['SpeedST'].max()  # Maximum speed from Speed Trap
        speed_trap = laps['SpeedFL'].max()  # Maximum speed from Fastest Lap
        driver_data.append({
            'driver': session.get_driver(drv)['LastName'],
            'top_speed': top_speed,
            'speed_trap': speed_trap
        })

    # Convert to DataFrame
    df = pd.DataFrame(driver_data)

    # Sorting data for plotting
    top_speeds = df[['driver', 'top_speed']].sort_values(by='top_speed', ascending=False).reset_index(drop=True)
    speed_traps = df[['driver', 'speed_trap']].sort_values(by='speed_trap', ascending=False).reset_index(drop=True)

    # 4. Data Analysis and Visualization

    # Define a function to annotate the bars
    def annotate_bars(ax, df, column):
        for i, (driver, value) in enumerate(zip(df['driver'], df[column])):
            ax.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom')

    # Define a function to add a watermark
    def add_watermark(fig, text, alpha=0.5):
        fig.text(0.5, 0.5, text, fontsize=40, color='gray', ha='center', va='center', alpha=alpha, rotation=30)

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Top Speed Visualization
    sns.barplot(x='driver', y='top_speed', data=top_speeds.head(10), palette='Blues_d', ax=ax1)
    annotate_bars(ax1, top_speeds.head(10), 'top_speed')
    ax1.set_title('Top 10 Drivers by Top Speed', fontsize=16)
    ax1.set_xlabel('Driver', fontsize=14)
    ax1.set_ylabel('Top Speed (km/h)', fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    # Highlight the top 3 drivers
    top_3_speeds = top_speeds.head(3)
    for i, row in top_3_speeds.iterrows():
        ax1.bar(row['driver'], row['top_speed'], color=['red', 'orange', 'yellow'][i])

    # Speed Trap Visualization
    sns.barplot(x='driver', y='speed_trap', data=speed_traps.head(10), palette='Greens_d', ax=ax2)
    annotate_bars(ax2, speed_traps.head(10), 'speed_trap')
    ax2.set_title('Top 10 Drivers by Speed Trap', fontsize=16)
    ax2.set_xlabel('Driver', fontsize=14)
    ax2.set_ylabel('Speed Trap (km/h)', fontsize=14)
    ax2.tick_params(axis='x', rotation=45)
    # Highlight the top 3 drivers
    top_3_traps = speed_traps.head(3)
    for i, row in top_3_traps.iterrows():
        ax2.bar(row['driver'], row['speed_trap'], color=['red', 'orange', 'yellow'][i])

    # Add watermark
    add_watermark(fig, 'F1 DATA IQ')

    plt.tight_layout()
    plt.savefig(top_speed_path)

    # New Feature: Average Speed Comparison

    # Calculate average top speed and speed trap for top 10 drivers
    average_top_speed = top_speeds['top_speed'].head(10).mean()
    average_speed_trap = speed_traps['speed_trap'].head(10).mean()

    # Prepare data for comparison
    average_speeds = pd.DataFrame({
        'Metric': ['Top Speed', 'Speed Trap'],
        'Average Speed (km/h)': [average_top_speed, average_speed_trap]
    })

    # Plot Average Speed Comparison
    plt.figure(figsize=(10, 6))
    ax3 = sns.barplot(x='Metric', y='Average Speed (km/h)', data=average_speeds, palette='coolwarm')
    for i, value in enumerate(average_speeds['Average Speed (km/h)']):
        ax3.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom')
    ax3.set_title('Average Speeds of Top 10 Drivers', fontsize=16)
    ax3.set_ylabel('Average Speed (km/h)', fontsize=14)

    # Add watermark
    add_watermark(plt.gcf(), 'F1 DATA IQ')

    plt.tight_layout()
    plt.savefig(speed_trap_path)

    # New Feature: Lap Time Comparison

    # Extract lap times for the top 3 drivers
    top_3_drivers = top_speeds['driver'].head(3)
    lap_times_data = []

    for driver in top_3_drivers:
        laps = session.laps.pick_driver(driver)
        lap_times = laps['LapTime'].dt.total_seconds()
        for lap_time in lap_times:
            lap_times_data.append({'driver': driver, 'lap_time': lap_time})

    # Convert to DataFrame
    lap_times_df = pd.DataFrame(lap_times_data)

    # Plot Lap Time Comparison
    plt.figure(figsize=(12, 8))
    ax4 = sns.boxplot(x='driver', y='lap_time', data=lap_times_df, palette='Set2')
    ax4.set_title('Lap Time Comparison of Top 3 Drivers', fontsize=16)
    ax4.set_xlabel('Driver', fontsize=14)
    ax4.set_ylabel('Lap Time (seconds)', fontsize=14)

    # Add annotations
    for driver in top_3_drivers:
        median_lap_time = lap_times_df[lap_times_df['driver'] == driver]['lap_time'].median()
        ax4.text(driver, median_lap_time, f'{median_lap_time:.2f}', ha='center', va='center', color='black', weight='bold')

    # Add watermark
    add_watermark(plt.gcf(), 'F1 DATA IQ')

    plt.tight_layout()
    # plt.savefig("test2.png")

    # New Feature: Sector Time Comparison for Top 3 Drivers

    # Extract sector times for the top 3 drivers
    sector_times_data = []

    for driver in top_3_drivers:
        laps = session.laps.pick_driver(driver)
        for _, lap in laps.iterlaps():
            sector_times_data.append({
                'driver': driver,
                'sector': 'Sector 1',
                'time': lap['Sector1Time'].total_seconds() if pd.notna(lap['Sector1Time']) else None
            })
            sector_times_data.append({
                'driver': driver,
                'sector': 'Sector 2',
                'time': lap['Sector2Time'].total_seconds() if pd.notna(lap['Sector2Time']) else None
            })
            sector_times_data.append({
                'driver': driver,
                'sector': 'Sector 3',
                'time': lap['Sector3Time'].total_seconds() if pd.notna(lap['Sector3Time']) else None
            })

    # Convert to DataFrame
    sector_times_df = pd.DataFrame(sector_times_data)

    # Plot Sector Time Comparison
    plt.figure(figsize=(14, 10))
    ax5 = sns.boxplot(x='sector', y='time', hue='driver', data=sector_times_df, palette='Set1')
    ax5.set_title('Sector Time Comparison of Top 3 Drivers', fontsize=16)
    ax5.set_xlabel('Sector', fontsize=14)
    ax5.set_ylabel('Sector Time (seconds)', fontsize=14)

    # Add watermark
    add_watermark(plt.gcf(), 'F1 DATA IQ')

    plt.tight_layout()
    plt.show()

    # New Feature: Summary Table for Key Statistics

    # Calculate key statistics
    summary_data = {
        'Driver': top_3_drivers,
        'Top Speed (km/h)': top_speeds['top_speed'].head(3).values,
        'Speed Trap (km/h)': speed_traps['speed_trap'].head(3).values,
        'Average Lap Time (seconds)': [lap_times_df[lap_times_df['driver'] == driver]['lap_time'].mean() for driver in top_3_drivers]
    }

    summary_df = pd.DataFrame(summary_data)

    # Display summary table
    plt.figure(figsize=(8, 4))
    plt.table(cellText=summary_df.values, colLabels=summary_df.columns, cellLoc='center', loc='center')
    plt.axis('off')
    plt.title('Summary Statistics for Top 3 Drivers', fontsize=16)

    # Add watermark
    add_watermark(plt.gcf(), 'F1 DATA IQ')

    plt.tight_layout()
    # plt.savefig("test3.png")
    return top_speed_path, speed_trap_path

def overtake(year, gp, identifier):
    session = ff1.get_session(year, gp, identifier)
    session.load()
    laps = session.laps

    def lap_involves_pit_stop(lap: Laps) -> bool:
        """Check if a lap involves a pit stop."""
        return lap['PitOutTime'].notna().any() or lap['PitInTime'].notna().any()

    overtakes = {}

    for lap_number in range(2, int(max(laps['LapNumber'])) + 1):
        current_lap = laps.pick_lap(lap_number)
        previous_lap = laps.pick_lap(lap_number - 1)
        
        for driver in current_lap['Driver'].unique():
            current_driver_lap = current_lap.pick_driver(driver)
            previous_driver_lap = previous_lap.pick_driver(driver)
            
            if lap_involves_pit_stop(current_driver_lap) or lap_involves_pit_stop(previous_driver_lap):
                continue
            
            current_position = current_driver_lap['Position'].values[0]
            previous_position = previous_driver_lap['Position'].values[0]
            
            if current_position < previous_position:
                overtakes[driver] = overtakes.get(driver, 0) + 1

    # Plotting adjustments
    drivers = list(overtakes.keys())
    overtake_counts = [overtakes[driver] for driver in drivers]
    max_overtakes = max(overtake_counts) if overtakes else 0
    colors = plt.cm.viridis(np.linspace(0, 1, len(drivers)))

    plt.figure(figsize=(10, 6))
    bars = plt.barh(drivers, overtake_counts, color=colors)

    # Add watermarks
    plt.text(0.5, 0.02, 'F1Datas.Com', fontsize=12, color='black', ha='center', va='bottom', alpha=0.5, transform=plt.gca().transAxes)
    plt.text(0.5, 0.98, 'F1 Data IQ', fontsize=12, color='black', ha='center', va='top', transform=plt.gca().transAxes)

    plt.xlabel('Number of Overtakes', fontsize=12)
    plt.ylabel('Drivers', fontsize=12)
    plt.title('Genuine Overtakes by Each Driver (Excluding Pit Stops)', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.xlim(0, max_overtakes)  # Set x-axis limits

    # Adding the count above each bar
    for bar, count in zip(bars, overtake_counts):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{count}', 
                va='center', ha='left', fontsize=10, color='blue')

    plt.tight_layout()
    overtake_path = f"{year}-{gp}-{identifier}-overtake.png"
    plt.savefig(overtake_path)

def map_viz(year, gp, identifier, driver):
    colormap = plt.cm.viridis

    # Load session data
    session = ff1.get_session(year, gp, identifier)
    weekend = session.event
    session.load()
    lap = session.laps.pick_driver(driver).pick_fastest()

    # Extract telemetry data
    x = lap.telemetry['X']
    y = lap.telemetry['Y']
    speed = lap.telemetry['Speed']

    # Create line segments for track visualization
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot background track line with markers
    ax.plot(x, y, color='lightgrey', linestyle='-', marker='o', markersize=2, markerfacecolor='black', linewidth=2, zorder=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(speed.min(), speed.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linewidth=4, zorder=2)
    lc.set_array(speed)
    line = ax.add_collection(lc)

    # Add color bar as legend with customizations
    cbar = plt.colorbar(line, ax=ax, orientation='horizontal', pad=0.04)
    cbar.set_label('Speed (m/s)')
    cbar.ax.tick_params(labelsize=12)

    # Add driver's initials
    ax.text(0.95, 0.05, driver, fontsize=16, color='black', ha='center', va='bottom', transform=ax.transAxes)

    # Add watermarks with improved appearance
    plt.text(0.98, 0.02, 'F1Datas.com', fontsize=10, color='black', ha='right', va='bottom', alpha=0.5, transform=ax.transAxes)
    plt.text(0.98, 0.98, 'F1 Data IQ', fontsize=10, color='black', ha='right', va='top', transform=ax.transAxes)

    # Add title with more information
    ax.set_title(f'{weekend.name} {year} - {identifier} - {driver} - Speed Visualization', fontsize=20)

    # Add labels and grid lines with enhanced appearance
    ax.set_xlabel('X Position (m)', fontsize=16)
    ax.set_ylabel('Y Position (m)', fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.7, linewidth=0.5)

    # Adjust figure spacing
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    # Show plot
    viz_path = f"{year}-{gp}-{identifier}-map_viz.png"
    plt.savefig(viz_path)


# start = time.time()
# try:
#     test = overtake(2024, 'Bahrain Grand Prix', "R")
# except Exception as e:
#     print(e)
# end = time.time()
# print(end - start)
