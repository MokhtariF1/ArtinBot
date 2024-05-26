import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
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
# start = time.time()
# try:
#     test = top_speed(200, 'jjlj', "s")
# except Exception as e:
#     print(e)
# end = time.time()
# print(end - start)
