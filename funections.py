import fastf1 as ff1
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

# start = time.time()
# try:
#     test = speed_rpm_delta(2024, 'Bahrain Grand Prix', "R", "VER", "HAM")
# except Exception as e:
#     print(e)
# end = time.time()
# print(end - start)
