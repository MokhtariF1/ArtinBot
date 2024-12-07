from datetime import datetime

import fastf1 as ff1
import pycountry
import requests
from fastf1 import plotting
from fastf1.core import Laps
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import seaborn as sns
import time
import random
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

    # Top Speed Visualization
    plt.figure(figsize=(12, 8))
    ax1 = sns.barplot(x='driver', y='top_speed', data=top_speeds, palette='Blues_d')
    annotate_bars(ax1, top_speeds, 'top_speed')
    ax1.set_title('Drivers by Top Speed', fontsize=16)
    ax1.set_xlabel('Driver', fontsize=14)
    ax1.set_ylabel('Top Speed (km/h)', fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(top_speed_path)

    # Speed Trap Visualization
    plt.figure(figsize=(12, 8))
    ax2 = sns.barplot(x='driver', y='speed_trap', data=speed_traps, palette='Greens_d')
    annotate_bars(ax2, speed_traps, 'speed_trap')
    ax2.set_title('Drivers by Speed Trap', fontsize=16)
    ax2.set_xlabel('Driver', fontsize=14)
    ax2.set_ylabel('Speed Trap (km/h)', fontsize=14)
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(speed_trap_path)

    # Average Speed Comparison for all drivers

    # Calculate average top speed and speed trap for all drivers
    average_top_speed = top_speeds['top_speed'].mean()
    average_speed_trap = speed_traps['speed_trap'].mean()

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
    ax3.set_title('Average Speeds of All Drivers', fontsize=16)
    ax3.set_ylabel('Average Speed (km/h)', fontsize=14)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(top_speed)

    # Lap Time Comparison for all drivers

    # Extract lap times for all drivers
    lap_times_data = []

    for driver in top_speeds['driver']:
        laps = session.laps.pick_driver(driver)
        lap_times = laps['LapTime'].dt.total_seconds()
        for lap_time in lap_times:
            lap_times_data.append({'driver': driver, 'lap_time': lap_time})

    # Convert to DataFrame
    lap_times_df = pd.DataFrame(lap_times_data)

    # Plot Lap Time Comparison
    plt.figure(figsize=(12, 8))
    ax4 = sns.boxplot(x='driver', y='lap_time', data=lap_times_df, palette='Set2')
    ax4.set_title('Lap Time Comparison of All Drivers', fontsize=16)
    ax4.set_xlabel('Driver', fontsize=14)
    ax4.set_ylabel('Lap Time (seconds)', fontsize=14)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(top_speed_path)

    # Sector Time Comparison for all drivers

    # Extract sector times for all drivers
    sector_times_data = []

    for driver in top_speeds['driver']:
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
    ax5.set_title('Sector Time Comparison of All Drivers', fontsize=16)
    ax5.set_xlabel('Sector', fontsize=14)
    ax5.set_ylabel('Sector Time (seconds)', fontsize=14)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(top_speed_path)

    # Summary Table for Key Statistics for all drivers

    # Calculate key statistics
    summary_data = {
        'Driver': top_speeds['driver'],
        'Top Speed (km/h)': top_speeds['top_speed'].values,
        'Speed Trap (km/h)': speed_traps['speed_trap'].values,
        'Average Lap Time (seconds)': [lap_times_df[lap_times_df['driver'] == driver]['lap_time'].mean() for driver in top_speeds['driver']]
    }

    summary_df = pd.DataFrame(summary_data)

    # Display summary table
    plt.figure(figsize=(15, 10))
    plt.table(cellText=summary_df.values, colLabels=summary_df.columns, cellLoc='center', loc='center')
    plt.axis('off')
    plt.title('Summary Statistics for All Drivers', fontsize=16)
    plt.tight_layout()
    add_watermark(plt.gcf(), 'F1 DATA IQ')
    plt.savefig(speed_trap_path)

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
    viz_path = f"{year}-{gp}-{identifier}-{driver}-map_viz.png"
    plt.savefig(viz_path)

def speed_rpm_delta(year, gp, identifier, driver_one, driver_two):
    session = ff1.get_session(year, gp, identifier)
    session.load()
    rpm_path = f"{year}-{gp}-{identifier}-{driver_one}-{driver_two}-rpm.png"
    # Select drivers
    driver_1 = driver_one  # Example driver code
    driver_2 = driver_two  # Example driver code

    # Get fastest laps
    fastest_lap_driver_1 = session.laps.pick_driver(driver_1).pick_fastest()
    fastest_lap_driver_2 = session.laps.pick_driver(driver_2).pick_fastest()

    # Get teams and print them for debugging
    team_driver_1 = fastest_lap_driver_1['Team']
    team_driver_2 = fastest_lap_driver_2['Team']

    # Define team colors (make sure names match with the data)
    team_colors = {
        'Red Bull Racing': '#1E41FF', 
        'Mercedes': '#00D2BE', 
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Alpine': '#0090FF',
        'AlphaTauri': '#4E7C9B',
        'Aston Martin': '#006F62',
        'Williams': '#005AFF',
        'Alfa Romeo': '#900000',
        'Haas': '#FFFFFF',
        'Haas F1 Team': "#FFFFFF",
        'RB': "#6692ff",
        "Kick Sauber": "#52e252",
    }

    # Check if both drivers are from the same team
    if team_driver_1 == team_driver_2:
        team_driver_2 = random.choice([team for team in team_colors.keys() if team != team_driver_1])

    # Get telemetry data
    telemetry_driver_1 = fastest_lap_driver_1.get_car_data().add_distance()
    telemetry_driver_2 = fastest_lap_driver_2.get_car_data().add_distance()

    # Calculate delta time between the drivers
    delta_time, ref_tel, compare_tel = ff1.utils.delta_time(fastest_lap_driver_1, fastest_lap_driver_2)

    # Convert lap times to formatted string
    def format_lap_time(lap_time):
        minutes = int(lap_time.total_seconds() // 60)
        seconds = lap_time.total_seconds() % 60
        return f"{minutes}:{seconds:06.3f}"

    lap_time_driver_1 = format_lap_time(fastest_lap_driver_1['LapTime'])
    lap_time_driver_2 = format_lap_time(fastest_lap_driver_2['LapTime'])

    # Plotting
    fig, ax = plt.subplots(3, 1, figsize=(12, 18), facecolor='black')
    fig.suptitle(f'Comparison of Fastest Laps: {driver_1} vs {driver_2}', color='white', fontsize=16, fontweight='bold')

    # Speed
    ax[0].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=f'{driver_1} Speed', color=team_colors[team_driver_1], linewidth=2)
    ax[0].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=f'{driver_2} Speed', color=team_colors[team_driver_2], linewidth=2)
    ax[0].set_facecolor('black')
    ax[0].set_ylabel('Speed (km/h)', color='white', fontsize=12, fontweight='bold')
    ax[0].set_title('Speed Comparison', color='white', fontsize=14, fontweight='bold')
    ax[0].legend(facecolor='black', edgecolor='white', fontsize=12, labelcolor=[team_colors[team_driver_1], team_colors[team_driver_2]])
    ax[0].grid(True, color='gray')
    ax[0].tick_params(axis='x', colors='white')
    ax[0].tick_params(axis='y', colors='white')

    # Mark max speed points
    max_speed_driver_1 = telemetry_driver_1['Speed'].max()
    max_speed_driver_2 = telemetry_driver_2['Speed'].max()
    max_speed_dist_driver_1 = telemetry_driver_1[telemetry_driver_1['Speed'] == max_speed_driver_1]['Distance'].iloc[0]
    max_speed_dist_driver_2 = telemetry_driver_2[telemetry_driver_2['Speed'] == max_speed_driver_2]['Distance'].iloc[0]
    ax[0].plot(max_speed_dist_driver_1, max_speed_driver_1, 'o', color=team_colors[team_driver_1])
    ax[0].plot(max_speed_dist_driver_2, max_speed_driver_2, 'o', color=team_colors[team_driver_2])
    ax[0].annotate(f'Max {driver_1} Speed: {max_speed_driver_1} km/h', xy=(max_speed_dist_driver_1, max_speed_driver_1), xytext=(max_speed_dist_driver_1 + 100, max_speed_driver_1 - 50), arrowprops=dict(facecolor=team_colors[team_driver_1], shrink=0.05), color=team_colors[team_driver_1], fontsize=10, fontweight='bold')
    ax[0].annotate(f'Max {driver_2} Speed: {max_speed_driver_2} km/h', xy=(max_speed_dist_driver_2, max_speed_driver_2), xytext=(max_speed_dist_driver_2 + 100, max_speed_driver_2 - 50), arrowprops=dict(facecolor=team_colors[team_driver_2], shrink=0.05), color=team_colors[team_driver_2], fontsize=10, fontweight='bold')

    # Add trend lines to speed plot
    z1 = np.polyfit(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], 1)
    p1 = np.poly1d(z1)
    ax[0].plot(telemetry_driver_1['Distance'], p1(telemetry_driver_1['Distance']), linestyle='--', color=team_colors[team_driver_1], alpha=0.3)

    z2 = np.polyfit(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], 1)
    p2 = np.poly1d(z2)
    ax[0].plot(telemetry_driver_2['Distance'], p2(telemetry_driver_2['Distance']), linestyle='--', color=team_colors[team_driver_2], alpha=0.3)

    # RPM
    ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=f'{driver_1} RPM', color=team_colors[team_driver_1], linewidth=2)
    ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=f'{driver_2} RPM', color=team_colors[team_driver_2], linewidth=2)
    ax[1].set_facecolor('black')
    ax[1].set_ylabel('RPM', color='white', fontsize=12, fontweight='bold')
    ax[1].set_title('RPM Comparison', color='white', fontsize=14, fontweight='bold')
    ax[1].legend(facecolor='black', edgecolor='white', fontsize=12, labelcolor=[team_colors[team_driver_1], team_colors[team_driver_2]])
    ax[1].grid(True, color='gray')
    ax[1].tick_params(axis='x', colors='white')
    ax[1].tick_params(axis='y', colors='white')

    # Mark max RPM points
    max_rpm_driver_1 = telemetry_driver_1['RPM'].max()
    max_rpm_driver_2 = telemetry_driver_2['RPM'].max()
    max_rpm_dist_driver_1 = telemetry_driver_1[telemetry_driver_1['RPM'] == max_rpm_driver_1]['Distance'].iloc[0]
    max_rpm_dist_driver_2 = telemetry_driver_2[telemetry_driver_2['RPM'] == max_rpm_driver_2]['Distance'].iloc[0]
    ax[1].plot(max_rpm_dist_driver_1, max_rpm_driver_1, 'o', color=team_colors[team_driver_1])
    ax[1].plot(max_rpm_dist_driver_2, max_rpm_driver_2, 'o', color=team_colors[team_driver_2])
    ax[1].annotate(f'Max {driver_1} RPM: {max_rpm_driver_1}', xy=(max_rpm_dist_driver_1, max_rpm_driver_1), xytext=(max_rpm_dist_driver_1 + 100, max_rpm_driver_1 - 500), arrowprops=dict(facecolor=team_colors[team_driver_1], shrink=0.05), color=team_colors[team_driver_1], fontsize=10, fontweight='bold')
    ax[1].annotate(f'Max {driver_2} RPM: {max_rpm_driver_2}', xy=(max_rpm_dist_driver_2, max_rpm_driver_2), xytext=(max_rpm_dist_driver_2 + 100, max_rpm_driver_2 - 500), arrowprops=dict(facecolor=team_colors[team_driver_2], shrink=0.05), color=team_colors[team_driver_2], fontsize=10, fontweight='bold')

    # Add trend lines to RPM plot
    z3 = np.polyfit(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], 1)
    p3 = np.poly1d(z3)
    ax[1].plot(telemetry_driver_1['Distance'], p3(telemetry_driver_1['Distance']), linestyle='--', color=team_colors[team_driver_1], alpha=0.3)

    z4 = np.polyfit(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], 1)
    p4 = np.poly1d(z4)
    ax[1].plot(telemetry_driver_2['Distance'], p4(telemetry_driver_2['Distance']), linestyle='--', color=team_colors[team_driver_2], alpha=0.3)

    # Delta
    ax[2].plot(ref_tel['Distance'], delta_time, label='Delta Time', color='lime', linewidth=2)
    ax[2].axhline(y=0, color=team_colors[team_driver_1], linestyle='-', linewidth=2)
    ax[2].set_facecolor('black')
    ax[2].set_ylabel('Delta Time (s)', color='white', fontsize=12, fontweight='bold')
    ax[2].set_xlabel('Distance (m)', color='white', fontsize=12, fontweight='bold')
    ax[2].set_title('Delta Time Comparison', color='white', fontsize=14, fontweight='bold')
    ax[2].legend(facecolor='black', edgecolor='white', fontsize=12, labelcolor=['lime'])
    ax[2].grid(True, color='gray')
    ax[2].tick_params(axis='x', colors='white')
    ax[2].tick_params(axis='y', colors='white')

    # Add horizontal lines to delta plot
    ax[2].axhline(y=0.1, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax[2].axhline(y=-0.1, color='red', linestyle='--', linewidth=1, alpha=0.7)

    # Adding start and end lines
    for a in ax:
        a.axvline(x=telemetry_driver_1['Distance'].iloc[0], color='white', linestyle='--', linewidth=1)
        a.axvline(x=telemetry_driver_1['Distance'].iloc[-1], color='white', linestyle='--', linewidth=1)

    # Adding lap times
    lap_time_text = f"{driver_1} Lap Time: {lap_time_driver_1}\n{driver_2} Lap Time: {lap_time_driver_2}"
    plt.figtext(0.99, 0.01, lap_time_text, horizontalalignment='right', color='white', fontsize=12, backgroundcolor='black')

    # Adding watermark
    fig.text(0.5, 0.5, 'F1 DATA IQ', fontsize=40, color='white', ha='center', va='center', alpha=0.1, rotation=45)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(rpm_path)

def map_brake(year, gp, identifier, driver):
    # Load session data
    session = ff1.get_session(year, gp, identifier)
    weekend = session.event
    session.load()

    # Extract fastest lap for the driver
    lap = session.laps.pick_driver(driver).pick_fastest()

    # Extract telemetry data
    x = lap.telemetry['X']
    y = lap.telemetry['Y']
    brake = lap.telemetry['Brake']
    time = lap.telemetry['Time']

    # Remove duplicate x values
    unique_indices = np.unique(x, return_index=True)[1]
    x_unique = x.iloc[np.sort(unique_indices)]
    y_unique = y.iloc[np.sort(unique_indices)]
    brake_unique = brake.iloc[np.sort(unique_indices)]
    time_unique = time.iloc[np.sort(unique_indices)]

    # Create line segments for track visualization
    points = np.array([x_unique, y_unique]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)

    # Plot background track line
    ax.plot(x_unique, y_unique, color='gray', linestyle='-', linewidth=8, zorder=1)

    # Brake Visualization
    brake_cmap = plt.cm.Reds
    brake_norm = plt.Normalize(0, 1)

    # Create a collection with segments colored by brake intensity
    lc_brake = LineCollection(segments, cmap=brake_cmap, norm=brake_norm, linewidths=4, zorder=2)
    lc_brake.set_array(brake_unique)
    ax.add_collection(lc_brake)

    # Add color bar for brake intensity
    cbar_brake = plt.colorbar(lc_brake, ax=ax, orientation='horizontal', pad=0.05)
    cbar_brake.set_label('Brake Intensity')

    # Add title and labels
    ax.set_title(f'{weekend.name} {year} - {driver} - Brake Visualization', fontsize=20, fontweight='bold')
    ax.set_xlabel('X Position (m)', fontsize=14)
    ax.set_ylabel('Y Position (m)', fontsize=14)

    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.7)

    # Add watermarks
    plt.text(0.5, 0.02, 'F1Datas.Com', fontsize=12, color='black', ha='center', va='bottom', alpha=0.7,
            transform=plt.gca().transAxes)
    plt.text(0.5, 0.98, 'F1 Data IQ', fontsize=12, color='black', ha='center', va='top', transform=plt.gca().transAxes)

    # Set aspect of the plot to be equal
    ax.set_aspect('equal', 'box')

    # Tight layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Show plot
    map_brake_path = f"{year}-{gp}-{identifier}-{driver}-map_brake"
    plt.savefig(map_brake_path)


def lap_times(year, gp, identifire):
    # enabling misc_mpl_mods will turn on minor grid lines that clutters the plot
    plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False)

    ###############################################################################
    # Load the race session

    race = ff1.get_session(year, gp, identifire)
    race.load()

    ###############################################################################
    # Get all the laps for the point finishers only.
    # Filter out slow laps (yellow flag, VSC, pitstops etc.)
    # as they distort the graph axis.
    point_finishers = race.drivers[:10]
    driver_laps = race.laps.pick_drivers(point_finishers).pick_quicklaps()
    driver_laps = driver_laps.reset_index()

    ###############################################################################
    # To plot the drivers by finishing order,
    # we need to get their three-letter abbreviations in the finishing order.
    finishing_order = [race.get_driver(i)["Abbreviation"] for i in point_finishers]

    ###############################################################################
    # We need to modify the DRIVER_COLORS palette.
    # Its keys are the driver's full names but we need the keys to be the drivers'
    # three-letter abbreviations.
    # We can do this with the DRIVER_TRANSLATE mapping.
    driver_colors = {abv: plotting.DRIVER_COLORS[driver] for abv,
                    driver in plotting.DRIVER_TRANSLATE.items()}

    ###############################################################################
    # First create the violin plots to show the distributions.
    # Then use the swarm plot to show the actual laptimes.

    # create the figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Seaborn doesn't have proper timedelta support
    # so we have to convert timedelta to float (in seconds)
    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    sns.violinplot(data=driver_laps,
                x="Driver",
                y="LapTime(s)",
                hue="Driver",
                inner=None,
                density_norm="area",
                order=finishing_order,
                palette=driver_colors
                )

    sns.swarmplot(data=driver_laps,
                x="Driver",
                y="LapTime(s)",
                order=finishing_order,
                hue="Compound",
                palette=ff1.plotting.COMPOUND_COLORS,
                hue_order=["SOFT", "MEDIUM", "HARD", "WET"],
                linewidth=0,
                size=4,
                )
    # sphinx_gallery_defer_figures

    ###############################################################################
    # Make the plot more aesthetic
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"{year} {gp} Lap Time Distributions")
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    lap_times_path = f"{year}-{gp}-{identifire}-lap_times.png"
    plt.savefig(lap_times_path)


def down_force(year, gp, session_type):
    # Define team colors
    team_colors = {
        'Mercedes': '#00D2BE',
        'Red Bull Racing': '#1E41FF',
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Alpine': '#0090FF',
        'AlphaTauri': '#4E7C9B',
        'Aston Martin': '#006F62',
        'Williams': '#005AFF',
        'Alfa Romeo': '#900000',
        'RB': '#6692FF',
        'Kick Sauber': '#52E252',
        'Haas F1 Team': '#FFFFFF'
    }
    grand_prix = gp
    session = ff1.get_session(year, grand_prix, session_type)
    session.load()

    # Get all drivers
    drivers = session.drivers

    # Create a DataFrame to store results
    results = []

    for driver in drivers:
        driver_laps = session.laps.pick_driver(driver)
        fastest_lap = driver_laps.pick_fastest()
        
        if fastest_lap.empty or pd.isna(fastest_lap['DriverNumber']):
            print(f"Skipping driver {driver} due to invalid DriverNumber")
            continue
        
        try:
            telemetry = fastest_lap.get_car_data().add_distance()
        except KeyError as e:
            print(f"Skipping driver {driver} due to KeyError: {e}")
            continue
        
        speed_data = telemetry['Speed']
        
        average_speed = speed_data.mean()
        top_speed = speed_data.max()
        
        result = 100 * (average_speed / top_speed)
        
        driver_name = session.get_driver(driver)['LastName'][:3].upper()
        team_name = session.get_driver(driver)['TeamName']
        
        total_laps = len(driver_laps)  # Total laps completed by the driver
        sector_times = driver_laps[['Sector1Time', 'Sector2Time', 'Sector3Time']].mean()  # Average sector times
        
        results.append({
            'Driver': driver_name,
            'Average Speed': average_speed,
            'Top Speed': top_speed,
            'Result': result,
            'Team': team_name,
            'Total Laps': total_laps,
            'Avg Sector 1': sector_times['Sector1Time'].total_seconds(),
            'Avg Sector 2': sector_times['Sector2Time'].total_seconds(),
            'Avg Sector 3': sector_times['Sector3Time'].total_seconds()
        })

    # Convert results to DataFrame
    df_results = pd.DataFrame(results)

    # Sort the DataFrame by the Result column
    df_results = df_results.sort_values(by='Result', ascending=False)

    # Plot the results
    plt.figure(figsize=(16, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')

    bars = plt.bar(df_results['Driver'], df_results['Result'], color=[team_colors[team] for team in df_results['Team']])
    plt.xlabel('Driver', color='white')
    plt.ylabel('Performance (%)', color='white')
    plt.title(f'{grand_prix} {year} {session_type} Performance Comparison', color='white', fontsize=18)
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, axis='y', alpha=0.7)

    # Add the result value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', color='white')

    # Add average line
    mean_result = df_results['Result'].mean()
    plt.axhline(mean_result, color='red', linewidth=1.5, linestyle='--')
    plt.text(len(df_results) - 1, mean_result, f'Mean: {mean_result:.2f}', color='red', ha='center', va='bottom')

    # Add sector times to the plot
    for i, row in df_results.iterrows():
        plt.text(i, -5, f'S1: {row["Avg Sector 1"]:.2f}s\nS2: {row["Avg Sector 2"]:.2f}s\nS3: {row["Avg Sector 3"]:.2f}s', ha='center', va='top', color='white', fontsize=8, rotation=45)

    # Add team names below driver names
    for i, (driver, team) in enumerate(zip(df_results['Driver'], df_results['Team'])):
        plt.text(i, -15, team, ha='center', va='top', color='white', fontsize=10, rotation=45)

    # Add description text below the plot
    plt.figtext(0.5, -0.1, f"Data obtained from fastest lap telemetry in the {year} {grand_prix} GP race session using FAST F1 library", wrap=True, horizontalalignment='center', fontsize=12, color='white')
    plt.figtext(0.5, -0.15, "Performance calculated as 100 * (Average Speed / Top Speed) for each driver", wrap=True, horizontalalignment='center', fontsize=10, color='white')

    # Update and enlarge watermark
    plt.figtext(0.5, 0.5, 'F1 DATA IQ', fontsize=70, color='gray', ha='center', va='center', alpha=0.5, rotation=45)

    # Display the plot
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit description text

    down_force_path = f"{year}-{gp}-{session_type}-down_force.png"
    plt.savefig(down_force_path)
    return down_force_path
TEAM_COLORS = {
    'Mercedes': '#00D2BE',
    'Ferrari': '#DC0000',
    'Red Bull': '#1E41FF',
    'McLaren': '#FF8700',
    'Renault': '#FFF500',
    'AlphaTauri': '#4E7C9B',
    'Racing Point': '#F596C8',
    'Alfa Romeo': '#900000',
    'Haas': '#FFFFFF',
    'Williams': '#0082FA'
}

def load_session(year, grand_prix, session_type):
    # Load the session
    session = ff1.get_session(year, grand_prix, session_type)
    session.load()
    return session

def calculate_metrics(session):
    drivers = session.drivers
    zero_to_hundred_times = {}
    tire_compounds = {}
    team_colors = {}
    max_speeds = {}
    max_accelerations = {}

    for drv in drivers:
        driver_info = session.get_driver(drv)
        driver_code = driver_info['Abbreviation']
        team_name = driver_info['TeamName']
        
        try:
            # Load laps for the driver
            laps = session.laps.pick_driver(driver_code)
            
            # Assuming the race start is the first lap
            first_lap = laps.iloc[0]
            telemetry = first_lap.get_telemetry()
            
            # Get the tire compound used at the start
            tire_compounds[driver_code] = first_lap['Compound']
            team_colors[driver_code] = TEAM_COLORS.get(team_name, '#FFFFFF')  # Default to white if team color is not found
            
            # Filter necessary columns to avoid dtype issues
            telemetry = telemetry[['Time', 'Speed']]
            
            # Calculate acceleration
            telemetry['Acceleration'] = telemetry['Speed'].diff() / telemetry['Time'].diff().dt.total_seconds()
            
            # Find the time when speed goes from 0 to 100 km/h
            start_time = None
            end_time = None
            for i in range(1, len(telemetry)):
                if telemetry['Speed'].iloc[i] > 0 and start_time is None:
                    start_time = telemetry['Time'].iloc[i]
                if telemetry['Speed'].iloc[i] >= 100:
                    end_time = telemetry['Time'].iloc[i]
                    break
            
            if start_time is not None and end_time is not None:
                zero_to_hundred_time = end_time - start_time
                zero_to_hundred_times[driver_code] = round(zero_to_hundred_time.total_seconds(), 3)
            
            # Calculate max speed and acceleration
            max_speeds[driver_code] = telemetry['Speed'].max()
            max_accelerations[driver_code] = telemetry['Acceleration'].max()
        
        except Exception as e:
            print(f"Could not process driver {driver_code}: {e}")
    
    return zero_to_hundred_times, tire_compounds, team_colors, max_speeds, max_accelerations

def save_metrics(zero_to_hundred_times, max_speeds, max_accelerations, filename='metrics.csv'):
    metrics_df = pd.DataFrame({
        'Driver': zero_to_hundred_times.keys(),
        'Zero to Hundred Time': zero_to_hundred_times.values(),
        'Max Speed': max_speeds.values(),
        'Max Acceleration': max_accelerations.values()
    })
    metrics_df.to_csv(filename, index=False)

def plot_metrics(zero_to_hundred_times, tire_compounds, team_colors, max_speeds, max_accelerations, year, grand_prix, session_type):
    metrics_df = pd.DataFrame({
        'Driver': zero_to_hundred_times.keys(),
        'Zero to Hundred Time': zero_to_hundred_times.values(),
        'Max Speed': max_speeds.values(),
        'Max Acceleration': max_accelerations.values()
    })
    metrics_df['Tire Compound'] = metrics_df['Driver'].map(tire_compounds)
    metrics_df['Team Color'] = metrics_df['Driver'].map(team_colors)
    metrics_df = metrics_df.sort_values(by='Zero to Hundred Time')
    
    plotting.setup_mpl()
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#2e2e2e')
    ax.set_facecolor('#2e2e2e')

    bars = ax.barh(metrics_df['Driver'], metrics_df['Zero to Hundred Time'], color=metrics_df['Team Color'])
    ax.set_xlabel('Time (seconds)', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Driver', fontsize=14, fontweight='bold', color='white')
    ax.set_title(f'Time to Accelerate from 0 to 100 km/h with Tire Compounds\n{year} {grand_prix}', fontsize=24, fontweight='bold', color='white')
    ax.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for bar, tire in zip(bars, metrics_df['Tire Compound']):
        width = bar.get_width()
        label_y_pos = bar.get_y() + bar.get_height() / 2
        ax.text(width, label_y_pos, f'{width:.3f} ({tire})', va='center', ha='left', color='white', fontsize=12)

    # Add watermark
    fig.text(0.5, 0.5, 'F1 DATA IQ', fontsize=50, color='gray', ha='center', va='center', alpha=0.5, rotation=30)

    plt.tight_layout()
    reaction_path = f"{year}-{grand_prix}-{session_type}-reaction.png"
    plt.savefig(reaction_path)
    return fig, ax, reaction_path

def start_reaction(year, gp, identifire):
    session = load_session(year, gp, identifire)
    zero_to_hundred_times, tire_compounds, team_colors, max_speeds, max_accelerations = calculate_metrics(session)

    # Save metrics to CSV
    save_metrics(zero_to_hundred_times, max_speeds, max_accelerations)

    # Plot metrics
    fig, ax, reaction_path = plot_metrics(zero_to_hundred_times, tire_compounds, team_colors, max_speeds, max_accelerations, year, gp, identifire)
    return reaction_path
def all_data(year, gp, identifire, driver_one, driver_two):
    session = ff1.get_session(year, gp, identifire)
    session.load()
    path_list = []
    # Select the laps
    lap_leclerc = session.laps.pick_driver(driver_one).pick_fastest()
    lap_sainz = session.laps.pick_driver(driver_two).pick_fastest()

    # Get the telemetry data
    telemetry_leclerc = lap_leclerc.get_telemetry().add_distance()
    telemetry_sainz = lap_sainz.get_telemetry().add_distance()

    # Resample telemetry data to common distance points
    common_distance = np.linspace(0, min(telemetry_leclerc['Distance'].max(), telemetry_sainz['Distance'].max()), num=500)
    telemetry_leclerc_resampled = telemetry_leclerc.set_index('Distance').reindex(common_distance, method='nearest').reset_index()
    telemetry_sainz_resampled = telemetry_sainz.set_index('Distance').reindex(common_distance, method='nearest').reset_index()

    # Plot Speed comparison
    plotting.setup_mpl()
    fig, ax_speed = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor('#000000')
    ax_speed.set_facecolor('#111111')

    ax_speed.plot(telemetry_leclerc_resampled['Distance'], telemetry_leclerc_resampled['Speed'], label='LEC Speed', color='cyan', lw=2)
    ax_speed.plot(telemetry_sainz_resampled['Distance'], telemetry_sainz_resampled['Speed'], label='SAI Speed', color='orange', lw=2)

    ax_speed.set_xlabel('Distance (m)', fontsize=14, fontweight='bold', color='white')
    ax_speed.set_ylabel('Speed (km/h)', fontsize=14, fontweight='bold', color='white')
    ax_speed.set_title('Speed Comparison - 2024 Bahrain GP Qualifying', fontsize=24, fontweight='bold', color='white')
    ax_speed.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax_speed.legend(loc='upper right', fontsize=14, facecolor='black', edgecolor='white', framealpha=1)
    speed_comparison_path = f"{year}-{gp}-{identifire}-{driver_one}-{driver_two}_speed_comparison.png"
    plt.savefig(speed_comparison_path)
    path_list.append(speed_comparison_path)

    # Plot Gear comparison
    fig, ax_gear = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor('#000000')
    ax_gear.set_facecolor('#111111')

    ax_gear.plot(telemetry_leclerc_resampled['Distance'], telemetry_leclerc_resampled['nGear'], label='LEC Gear', color='cyan', lw=2)
    ax_gear.plot(telemetry_sainz_resampled['Distance'], telemetry_sainz_resampled['nGear'], label='SAI Gear', color='orange', lw=2)

    ax_gear.set_xlabel('Distance (m)', fontsize=14, fontweight='bold', color='white')
    ax_gear.set_ylabel('Gear', fontsize=14, fontweight='bold', color='white')
    ax_gear.set_title('Gear Comparison - 2024 Bahrain GP Qualifying', fontsize=24, fontweight='bold', color='white')
    ax_gear.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax_gear.legend(loc='upper right', fontsize=14, facecolor='black', edgecolor='white', framealpha=1)
    gear_comparison_path = f"{year}-{gp}-{identifire}-{driver_one}-{driver_two}_gear_comparison.png"
    plt.savefig(gear_comparison_path)
    path_list.append(gear_comparison_path)
    # Plot Brake comparison
    fig, ax_brake = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor('#000000')
    ax_brake.set_facecolor('#111111')

    ax_brake.plot(telemetry_leclerc_resampled['Distance'], telemetry_leclerc_resampled['Brake'], label='LEC Brake', color='cyan', lw=2)
    ax_brake.plot(telemetry_sainz_resampled['Distance'], telemetry_sainz_resampled['Brake'], label='SAI Brake', color='orange', lw=2)

    ax_brake.set_xlabel('Distance (m)', fontsize=14, fontweight='bold', color='white')
    ax_brake.set_ylabel('Brake', fontsize=14, fontweight='bold', color='white')
    ax_brake.set_title('Brake Comparison - 2024 Bahrain GP Qualifying', fontsize=24, fontweight='bold', color='white')
    ax_brake.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax_brake.legend(loc='upper right', fontsize=14, facecolor='black', edgecolor='white', framealpha=1)
    brake_comparison_path = f"{year}-{gp}-{identifire}-{driver_one}-{driver_two}_brake_comparison.png"
    plt.savefig(brake_comparison_path)
    path_list.append(brake_comparison_path)
    # Plot Throttle comparison
    fig, ax_throttle = plt.subplots(figsize=(18, 12))
    fig.patch.set_facecolor('#000000')
    ax_throttle.set_facecolor('#111111')

    ax_throttle.plot(telemetry_leclerc_resampled['Distance'], telemetry_leclerc_resampled['Throttle'], label='LEC Throttle', color='cyan', lw=2)
    ax_throttle.plot(telemetry_sainz_resampled['Distance'], telemetry_sainz_resampled['Throttle'], label='SAI Throttle', color='orange', lw=2)

    ax_throttle.set_xlabel('Distance (m)', fontsize=14, fontweight='bold', color='white')
    ax_throttle.set_ylabel('Throttle (%)', fontsize=14, fontweight='bold', color='white')
    ax_throttle.set_title('Throttle Comparison - 2024 Bahrain GP Qualifying', fontsize=24, fontweight='bold', color='white')
    ax_throttle.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
    ax_throttle.legend(loc='upper right', fontsize=14, facecolor='black', edgecolor='white', framealpha=1)
    throttle_comparison_path = f"{year}-{gp}-{identifire}-{driver_one}-{driver_two}_throttle_comparison.png"
    plt.savefig(throttle_comparison_path)
    path_list.append(throttle_comparison_path)
    
    return path_list
def strategy(year, gp, identifire):
    grand_prix = gp

    # Load the race session
    session = ff1.get_session(year, grand_prix, identifire)
    session.load()
    laps = session.laps

    # Get the list of driver numbers
    drivers = session.drivers

    # Convert driver numbers to three-letter abbreviations
    driver_abbreviations = []
    for driver in drivers:
        try:
            abbreviation = session.get_driver(driver)["Abbreviation"]
            driver_abbreviations.append(abbreviation)
        except KeyError:
            # Skip the driver if no abbreviation is found
            continue

    # Group laps by driver, stint number, and compound
    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()

    # Rename the LapNumber column to StintLength
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    # Create a figure and axes for the plot
    fig, ax = plt.subplots(figsize=(10, 12))

    # Plot the tire strategies for each driver
    for driver in driver_abbreviations:
        driver_stints = stints.loc[stints["Driver"] == driver]
        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            # Get the color of the tire compound
            compound_color = ff1.plotting.get_compound_color(row["Compound"], session=session)
            plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=compound_color,
                edgecolor="black"
            )
            previous_stint_end += row["StintLength"]

    # Additional plot settings for better readability
    plt.title(f"{year} {grand_prix} Grand Prix Strategies")
    plt.xlabel("Lap Number")
    plt.grid(False)
    ax.invert_yaxis()  # Invert the y-axis to show higher finishing drivers at the top

    # Remove unnecessary plot borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Add a watermark
    fig.text(0.5, 0.5, 'F1 DATA IQ', fontsize=50, color='gray', ha='center', va='center', alpha=0.3)

    plt.tight_layout()  # Improve layout
    plot_strategy_path = f"{year}-{gp}-{identifire}_strategy.png"
    plt.savefig(plot_strategy_path)  # Display the plot

    return plot_strategy_path

def all_info(year, grand_prix, identifire):
    # Load the race session
    session = ff1.get_session(year, grand_prix, identifire)
    session.load()

    # Get the list of driver numbers
    drivers = session.drivers

    # Convert driver numbers to three-letter abbreviations
    driver_abbreviations = []
    for driver in drivers:
        try:
            abbreviation = session.get_driver(driver)["Abbreviation"]
            driver_abbreviations.append(abbreviation)
        except KeyError:
            # Skip the driver if no abbreviation is found
            continue

    # Get the race results and print the columns to inspect
    results = session.results

    # Sort drivers based on their finishing positions
    sorted_results = results.sort_values(by='Position')
    # Verify the correct column name for driver identifiers

    # Assuming 'DriverNumber' is the correct column name
    top_10_drivers = sorted_results.head(10)['DriverNumber'].tolist()
    top_10_abbreviations = [session.get_driver(driver)["Abbreviation"] for driver in top_10_drivers]

    # Create a figure and axes for the plot
    fig, ax = plt.subplots(figsize=(10, 12))

    # Plot the G-Force for each of the top 10 drivers using telemetry data
    for driver in top_10_abbreviations:
        laps_driver = session.laps.pick_driver(driver)
        telemetry = laps_driver.get_car_data().add_distance()
        
        # Calculate the magnitude of G-Force
        telemetry['GForce'] = (telemetry['Throttle'] * telemetry['Brake']).abs()  # Simplified G-Force calculation
        
        ax.plot(telemetry['Distance'], telemetry['GForce'], label=driver)

    # Additional plot settings for better readability
    plt.title(f"{year} {grand_prix} Grand Prix Top 10 Drivers G-Force")
    plt.xlabel("Distance (m)")
    plt.ylabel("G-Force")
    plt.legend(title="Driver")
    plt.grid(True)

    # Add a watermark
    fig.text(0.5, 0.5, 'F1 DATA IQ', fontsize=50, color='gray', ha='center', va='center', alpha=0.3)

    plt.tight_layout()  # Improve layout
    all_info_path = f"{year}-{grand_prix}-{identifire}_all_info.png"
    plt.savefig(all_info_path)  # Display the plot
    
    return all_info_path

def driver_func_data(year, grand_prix, identifire, driver_one, driver_two):
    # Load the race session
    session = ff1.get_session(year, grand_prix, identifire)
    session.load()

    # Define the drivers to compare
    driver1_name = driver_one  # Hamilton
    driver2_name = driver_two  # Leclerc

    # Create a figure and axes for the plot
    fig, ax = plt.subplots(figsize=(10, 12))

    # Define a function to plot G-Force for a selected driver
    def plot_driver_g_force(driver_abbreviation, color):
        # Get laps and telemetry data for the driver
        laps_driver = session.laps.pick_driver(driver_abbreviation)
        telemetry = laps_driver.get_car_data().add_distance()
        
        # Calculate the magnitude of G-Force
        telemetry['GForce'] = (telemetry['Throttle'] * telemetry['Brake']).abs()  # Simplified G-Force calculation
        
        # Plot G-Force data
        ax.plot(telemetry['Distance'], telemetry['GForce'], label=driver_abbreviation, color=color)

    # Plot the G-Force for Hamilton and Leclerc
    plot_driver_g_force(driver1_name, 'blue')
    plot_driver_g_force(driver2_name, 'red')

    # Additional plot settings for better readability
    plt.title(f"{year} {grand_prix} Grand Prix G-Force Comparison: {driver_one} vs {driver_two}")
    plt.xlabel("Distance (m)")
    plt.ylabel("G-Force")
    plt.legend(title="Driver")
    plt.grid(True)

    # Add a watermark
    fig.text(0.5, 0.5, 'F1 DATA IQ', fontsize=50, color='gray', ha='center', va='center', alpha=0.3)

    plt.tight_layout()  # Improve layout
    driver_path = f"{year}-{grand_prix}-{identifire}-{driver_one}-{driver_two}_driver.png"
    plt.savefig(driver_path)  # Display the plot

    return driver_path
drivers = {
    "VER": "Max Verstappen",
    "HAM": "Lewis Hamilton",
    "LEC": "Charles Leclerc",
    "PER": "Sergio Pérez",
    "SAI": "Carlos Sainz",
    "NOR": "Lando Norris",
    "RIC": "Daniel Ricciardo",
    "ALO": "Fernando Alonso",
    "RUS": "George Russell",
    "GAS": "Pierre Gasly",
    "OCO": "Esteban Ocon",
    "BOT": "Valtteri Bottas",
    "TSU": "Yuki Tsunoda",
    "MAG": "Kevin Magnussen",
    "HUL": "Nico Hülkenberg",
    "ALB": "Alexander Albon",
    "STR": "Lance Stroll",
    "PIA": "Oscar Piastri",
    "ZHO": "Guanyu Zhou",
    "COL": "Franco Colapinto",
}

# Allow comparing multiple drivers
selected_driver_codes = ['VER']  # List of drivers to compare

# Helper function to format lap times
def format_lap_time(lap_time_seconds):
    if pd.isna(lap_time_seconds):
        return 'NAT'  # Not Available Time
    minutes = int(lap_time_seconds // 60)
    seconds = lap_time_seconds % 60
    return f"{minutes}:{seconds:06.3f}"  # Format as M:SS.mmm

# Helper function to format sector times (no minutes, only seconds)
def format_sector_time(sector_time_seconds):
    if pd.isna(sector_time_seconds):
        return 'NAN'  # Not Available Number
    return f"{sector_time_seconds:06.3f}"  # Format as SS.mmm

# Function to plot lap times and sectors
def plot_lap_times(lap_data, driver_names, year, gp):
    plt.figure(figsize=(10, 6))
    for driver, lap_info in lap_data.items():
        lap_numbers = lap_info['Lap Number']
        lap_times = lap_info['Lap Time Seconds']
        plt.plot(lap_numbers, lap_times, marker='o', label=driver_names[driver])

    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (Seconds)")
    plt.title(f"{year} {gp} Grand Prix - Lap Time Comparison")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.tight_layout()

# Main function to display and process lap times
def show_driver_lap_times(driver_codes, year, grand_prix, session_type):
    all_lap_data = {}
    fastest_lap = float('inf')
    fastest_lap_driver = ''
    driver_names = {code: drivers[code] for code in driver_codes}

    # Load session and process laps for each driver
    for driver_code in driver_codes:
        ses = ff1.get_session(year, grand_prix, session_type)
        ses.load()
        laps = ses.laps.pick_driver(driver_code).copy()

        if laps.empty:
            print(f"No data found for driver: {driver_code} in session {session_type}.")
            continue

        # Handling Qualifying sessions (Q1, Q2, Q3 assignment)
        if session_type == 'Q':
            q1_cutoff = ses.results['Q1'].max()
            q2_cutoff = ses.results['Q2'].max()
            laps['SessionPart'] = np.where(laps['LapTime'] <= q1_cutoff, 'Q1', 
                                           np.where(laps['LapTime'] <= q2_cutoff, 'Q2', 'Q3'))
        else:
            laps['SessionPart'] = session_type

        # Prepare lap data with sectors
        laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
        laps['FormattedLapTime'] = laps['LapTimeSeconds'].apply(format_lap_time)
        laps['LapNumber'] = laps['LapNumber'].astype(int)

        # Process sector times and format them as SS.mmm
        if 'Sector1Time' in laps and 'Sector2Time' in laps and 'Sector3Time' in laps:
            laps['Sector1Time'] = laps['Sector1Time'].dt.total_seconds().apply(format_sector_time)
            laps['Sector2Time'] = laps['Sector2Time'].dt.total_seconds().apply(format_sector_time)
            laps['Sector3Time'] = laps['Sector3Time'].dt.total_seconds().apply(format_sector_time)

        # Update the fastest lap across drivers
        valid_lap_times = laps['LapTimeSeconds'].dropna()
        if not valid_lap_times.empty:
            driver_fastest_lap = valid_lap_times.min()
            if driver_fastest_lap < fastest_lap:
                fastest_lap = driver_fastest_lap
                fastest_lap_driver = driver_code

        # Store lap data for this driver
        all_lap_data[driver_code] = {
            'Lap Number': laps['LapNumber'].tolist(),
            'Lap Time': laps['FormattedLapTime'].tolist(),
            'Lap Time Seconds': laps['LapTimeSeconds'].tolist(),
            'Session Part': laps['SessionPart'].tolist(),
            'Sector 1': laps.get('Sector1Time', []).tolist(),
            'Sector 2': laps.get('Sector2Time', []).tolist(),
            'Sector 3': laps.get('Sector3Time', []).tolist()
        }

    # Paginate the table display for large numbers of laps (18 rows per page)
    rows_per_page = 18
    images_list = []
    for driver_code, lap_data in all_lap_data.items():
        table_data = pd.DataFrame({
            'Lap Number': lap_data['Lap Number'],
            'Session Part': lap_data['Session Part'],
            'Lap Time': lap_data['Lap Time'],
            'Sector 1': lap_data['Sector 1'],
            'Sector 2': lap_data['Sector 2'],
            'Sector 3': lap_data['Sector 3'],
        })

        num_pages = (len(table_data) // rows_per_page) + 1

        for page in range(num_pages):
            fig, ax = plt.subplots(figsize=(12, 7))
            ax.axis('tight')
            ax.axis('off')

            # Get the rows for the current page
            start_row = page * rows_per_page
            end_row = min(start_row + rows_per_page, len(table_data))
            page_data = table_data.iloc[start_row:end_row]

            # Create a color list for alternating row colors
            colors = []
            for i in range(len(page_data)):
                if i % 2 == 0:
                    colors.append(['#f1f1f2'] * len(page_data.columns))  # Light gray
                else:
                    colors.append(['#ffffff'] * len(page_data.columns))  # White

            # Create the table
            mpl_table = ax.table(cellText=page_data.values,
                                 colLabels=table_data.columns,
                                 cellColours=colors,
                                 cellLoc='center',
                                 loc='center')

            mpl_table.auto_set_font_size(False)
            mpl_table.set_fontsize(10)
            mpl_table.scale(1.2, 1.2)

            # Bold the headers
            for key, cell in mpl_table.get_celld().items():
                if key[0] == 0:
                    cell.set_text_props(weight='bold', fontsize=12)
                    cell.set_facecolor('#c0c0c0')

            # Improved Title with Stylish Formatting
            title_driver_info = f"{drivers[driver_code]} ({session_type})"
            title_event_info = f"{year} {grand_prix} Grand Prix"
            title_page_info = f"Page {page + 1}/{num_pages}"

            # Stylish title: larger, bold, and color differentiation
            fig.suptitle(f"{title_event_info}\n{title_driver_info}\n{title_page_info}",
                         fontsize=18, weight='bold', color='darkblue', y=0.98, ha='center')

            # Improved summary: Fastest lap info with styling
            summary_text = (f"Fastest Lap: {format_lap_time(fastest_lap)} "
                            f"by {drivers[fastest_lap_driver]}")
            plt.figtext(0.5, 0.02, summary_text, wrap=True,
                        horizontalalignment='center', fontsize=13, color='green', weight='bold')

            # Add watermark
            plt.text(0.5, 0.5, 'F1 DATA IQ', fontsize=50, color='gray', alpha=0.2,
                     ha='center', va='center', rotation=30, transform=plt.gca().transAxes)

            plt.tight_layout()
            name = f"{year}-{grand_prix}-{session_type}-{page + 1}-lap_times_table.png"
            plt.savefig(name)
            images_list.append(name)
    # Optionally plot lap times
    plot_lap_times(all_lap_data, driver_names, year=year, gp=grand_prix)
    return images_list
def brake_configurations(year, gp, session_type):
    team_colors = {
        'Mercedes': '#00D2BE',
        'Red Bull Racing': '#1E41FF',
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Alpine': '#0090FF',
        'AlphaTauri': '#4E7C9B',
        'Aston Martin': '#006F62',
        'Williams': '#005AFF',
        'Alfa Romeo': '#900000',
        'RB': '#6692FF',
        'Kick Sauber': '#52E252',
        'Haas F1 Team': '#FFFFFF'
    }
    grand_prix = gp
    session = ff1.get_session(year, grand_prix, session_type)
    session.load()

    # Get all drivers
    drivers = session.drivers

    # Create a DataFrame to store results
    results = []

    for driver in drivers:
        driver_laps = session.laps.pick_driver(driver)
        fastest_lap = driver_laps.pick_fastest()
        
        if fastest_lap.empty or pd.isna(fastest_lap['DriverNumber']):
            print(f"Skipping driver {driver} due to invalid DriverNumber")
            continue
        
        try:
            telemetry = fastest_lap.get_car_data().add_distance()
        except KeyError as e:
            print(f"Skipping driver {driver} due to KeyError: {e}")
            continue
        
        # Brake and speed data
        brake_data = telemetry['Brake']  # 1 when braking, 0 when not
        speed_data = telemetry['Speed']
        
        # Calculate time spent braking (duration of braking)
        braking_duration = brake_data.sum() * (telemetry['Distance'].diff().mean() / speed_data.mean())
        
        # Total lap time in seconds
        lap_time_seconds = fastest_lap['LapTime'].total_seconds()
        
        # Brake efficiency: percentage of time spent braking
        brake_efficiency = (braking_duration / lap_time_seconds) * 100
        
        driver_name = session.get_driver(driver)['LastName'][:3].upper()
        team_name = session.get_driver(driver)['TeamName']
        
        results.append({
            'Driver': driver_name,
            'Brake Efficiency (%)': brake_efficiency,
            'Lap Time (s)': lap_time_seconds,
            'Team': team_name
        })

    # Convert results to DataFrame
    df_results = pd.DataFrame(results)

    # Sort the DataFrame by Brake Efficiency
    df_results = df_results.sort_values(by='Brake Efficiency (%)', ascending=False)

    # Plot the results
    plt.figure(figsize=(16, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')

    bars = plt.bar(df_results['Driver'], df_results['Brake Efficiency (%)'], color=[team_colors[team] for team in df_results['Team']])
    plt.xlabel('Driver', color='white')
    plt.ylabel('Brake Efficiency (%)', color='white')
    plt.title(f'{grand_prix} {year} {session_type} Brake Efficiency Comparison', color='white', fontsize=18)
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    plt.grid(color='gray', linestyle='--', linewidth=0.5, axis='y', alpha=0.7)

    # Add the brake efficiency value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', color='white')

    # Add average line
    mean_efficiency = df_results['Brake Efficiency (%)'].mean()
    plt.axhline(mean_efficiency, color='red', linewidth=1.5, linestyle='--')
    plt.text(len(df_results) - 1, mean_efficiency, f'Mean: {mean_efficiency:.2f}', color='red', ha='center', va='bottom')

    # Add team names below driver names
    for i, (driver, team) in enumerate(zip(df_results['Driver'], df_results['Team'])):
        plt.text(i, -2, team, ha='center', va='top', color='white', fontsize=10, rotation=45)

    # Add description text below the plot
    plt.figtext(0.5, -0.1, f"Data obtained from fastest lap telemetry in the {year} {grand_prix} GP race session using FAST F1 library", wrap=True, horizontalalignment='center', fontsize=12, color='white')
    plt.figtext(0.5, -0.15, "The plot shows the percentage of time each driver spent braking during their fastest lap", wrap=True, horizontalalignment='center', fontsize=10, color='white')

    # Update and enlarge watermark
    plt.figtext(0.5, 0.5, 'F1 DATA IQ', fontsize=70, color='gray', ha='center', va='center', alpha=0.5, rotation=45)

    # Display the plot
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit description text
    name = f"{year}-{grand_prix}-{session_type}-brake_configurations.png"
    plt.savefig(name)
    return name
def composite_perfomance(year, grand_prix, session_type):
    # Define team colors
    team_colors = {
        'Mercedes': '#00D2BE',
        'Red Bull Racing': '#1E41FF',
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Alpine': '#0090FF',
        'AlphaTauri': '#4E7C9B',
        'Aston Martin': '#006F62',
        'Williams': '#005AFF',
        'Alfa Romeo': '#900000',
        'RB': '#6692FF',
        'Kick Sauber': '#52E252',
        'Haas F1 Team': '#FFFFFF'
    }

    session = ff1.get_session(year, grand_prix, session_type)
    session.load()

    # Get all drivers
    drivers = session.drivers

    # Create a DataFrame to store results
    results = []

    for driver in drivers:
        driver_laps = session.laps.pick_driver(driver)
        fastest_lap = driver_laps.pick_fastest()
        
        if fastest_lap.empty or pd.isna(fastest_lap['DriverNumber']):
            print(f"Skipping driver {driver} due to invalid DriverNumber")
            continue
        
        try:
            telemetry = fastest_lap.get_car_data().add_distance()
        except KeyError as e:
            print(f"Skipping driver {driver} due to KeyError: {e}")
            continue
        
        # Speed, acceleration and brake data
        brake_data = telemetry['Brake']  # 1 when braking, 0 when not
        speed_data = telemetry['Speed']
        acceleration_data = speed_data.diff() / telemetry['Distance'].diff()  # Basic acceleration calculation
        
        # Calculate time spent braking (duration of braking)
        braking_duration = brake_data.sum() * (telemetry['Distance'].diff().mean() / speed_data.mean())
        
        # Total lap time in seconds
        lap_time_seconds = fastest_lap['LapTime'].total_seconds()
        
        # Brake efficiency: percentage of time spent braking
        brake_efficiency = (braking_duration / lap_time_seconds) * 100
        
        # Speed factor
        speed_factor = speed_data.mean()
        
        # Acceleration factor
        acceleration_factor = acceleration_data[acceleration_data > 0].mean()  # Acceleration (positive changes in speed)
        
        # Handling time (time spent at speeds lower than a threshold, indicating cornering)
        handling_threshold = speed_data.mean() * 0.7  # Assuming cornering happens at 70% of the average speed
        handling_time = len(speed_data[speed_data < handling_threshold]) * (telemetry['Distance'].diff().mean() / speed_data.mean())
        
        # Composite Performance Index
        composite_performance_index = (speed_factor * acceleration_factor) / (brake_efficiency + handling_time)
        
        driver_name = session.get_driver(driver)['LastName'][:3].upper()
        team_name = session.get_driver(driver)['TeamName']
        
        results.append({
            'Driver': driver_name,
            'Composite Performance Index': composite_performance_index,
            'Speed Factor': speed_factor,
            'Acceleration Factor': acceleration_factor,
            'Brake Efficiency (%)': brake_efficiency,
            'Handling Time (s)': handling_time,
            'Lap Time (s)': lap_time_seconds,
            'Team': team_name
        })

    # Convert results to DataFrame
    df_results = pd.DataFrame(results)

    # Sort the DataFrame by Composite Performance Index
    df_results = df_results.sort_values(by='Composite Performance Index', ascending=False)

    # Plot the results
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='black')
    ax.set_facecolor('black')

    # Bar chart for Composite Performance Index
    bars = plt.bar(df_results['Driver'], df_results['Composite Performance Index'], color=[team_colors[team] for team in df_results['Team']])
    plt.xlabel('Driver', color='white', fontsize=12)
    plt.ylabel('Composite Performance Index', color='white', fontsize=12)

    # Adjust title placement to be closer to the top
    plt.title(f'{grand_prix} {year} {session_type} - Composite Performance Index', color='white', fontsize=20, pad=20)
    plt.xticks(rotation=45, color='white', fontsize=10)
    plt.yticks(color='white', fontsize=10)
    plt.grid(color='gray', linestyle='--', linewidth=0.5, axis='y', alpha=0.7)

    # Add the composite performance index value on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', color='white')

    # Add average line for composite performance index
    mean_performance = df_results['Composite Performance Index'].mean()
    plt.axhline(mean_performance, color='red', linewidth=1.5, linestyle='--')
    plt.text(len(df_results) - 1, mean_performance, f'Mean: {mean_performance:.2f}', color='red', ha='center', va='bottom')

    # Add team names below driver names
    for i, (driver, team) in enumerate(zip(df_results['Driver'], df_results['Team'])):
        plt.text(i, -2, team, ha='center', va='top', color='white', fontsize=10, rotation=45)

    # Display the calculation formula at the bottom of the plot
    plt.figtext(0.5, 0.85, "Composite Performance Index = (Speed Factor * Acceleration Factor) / (Brake Efficiency + Handling Time)", wrap=True, horizontalalignment='center', fontsize=12, color='white')

    # Update and enlarge watermark
    plt.figtext(0.5, 0.5, 'F1 DATA IQ', fontsize=70, color='gray', ha='center', va='center', alpha=0.3, rotation=45)

    # Display the plot
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit description text
    name = f"{year}-{grand_prix}-{session_type}-composite_perfomance.png"
    plt.savefig(name)
    return name
def country_flag(country_name):
    try:
        # Get the country object from the country name
        country = pycountry.countries.lookup(country_name)
        # Get the ISO 3166-1 alpha-2 country code
        country_code = country.alpha_2
        # Convert to flag emoji
        flag_emoji = ''.join(chr(ord(character) + 0x1F1A5) for character in country_code)
        return flag_emoji
    except LookupError:
        return "🏴"

def check_date(date_str):
    # Convert the string to a datetime object
    input_date = datetime.strptime(date_str, '%Y-%m-%d')
    # Get the current date
    current_date = datetime.now()

    # Check if the input date has passed
    if input_date < current_date:
        return False
    else:
        # Calculate the difference in days
        days_remaining = (input_date - current_date).days
        return days_remaining + 1

def get_year_calender(year):
    url = f"https://ergast.com/api/f1/{year}.json"
    response = requests.get(url).json()
    races = response["MRData"]["RaceTable"]["Races"]
    text = f"🗓 The {year} F1 Grand Prix calendar:\n"
    date_checked = False
    for race in races:
        race_name = race["raceName"]
        race_date_er = race["date"]
        race_time = race["time"]
        time_obj = datetime.strptime(race_time, '%H:%M:%SZ')
        # Format it to "HH:MM"
        race_time = time_obj.strftime('%H:%M')
        # Convert the string to a datetime object
        date_obj = datetime.strptime(race_date_er, '%Y-%m-%d')
        # Format the date to "Mon D"
        race_date = date_obj.strftime('%b %d')
        country_name = race["Circuit"]["Location"]["country"]
        country_flag_emoji = country_flag(country_name)
        grand_alarm = ''
        if date_checked is False:
            ch_date = check_date(race_date_er)
            if ch_date is not False:
                grand_alarm = f"⬇️ Next Grand Prix is in {ch_date} days ⬇️"
        grand_text = f"{country_flag_emoji}{race_name}, {race_date} {race_time}"
        text += "\n" + grand_alarm + "\n" + grand_text
    return text
def next_grand_prix():
    url = f"https://ergast.com/api/f1/2024.json"
    response = requests.get(url).json()
    races = response["MRData"]["RaceTable"]["Races"]
    text = "🗓 The 2024 F1 {grand} Grand Prix calendar:\n"
    date_checked = False
    for race in races:
        race_name = race["raceName"]
        race_date_er = race["date"]
        race_time = race["time"]
        time_obj = datetime.strptime(race_time, '%H:%M:%SZ')
        # Format it to "HH:MM"
        race_time = time_obj.strftime('%H:%M')
        # Convert the string to a datetime object
        date_obj = datetime.strptime(race_date_er, '%Y-%m-%d')
        # Format the date to "Mon D"
        race_date = date_obj.strftime('%b %d')
        next_grand = None
        if date_checked is False:
            ch_date = check_date(race_date_er)
            if ch_date is not False:
                next_grand = race_name
                text += next_grand + "\n" + race_date + "\n" + race_time
    return text