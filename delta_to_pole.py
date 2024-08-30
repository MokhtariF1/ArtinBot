import fastf1
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

def load_session(year, round, session_type):
    try:
        session = fastf1.get_session(year, round, session_type)
        session.load()
        return session
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

def format_lap_time(lap_time):
    """Format lap time to '1:20.432' style."""
    minutes = lap_time.components.minutes
    seconds = lap_time.components.seconds
    milliseconds = lap_time.components.milliseconds
    return f"{minutes}:{seconds:02}.{milliseconds:03}"

def process_q3_data(session):
    # Determine the Q3 laps based on lap timings
    q3_laps = session.laps[session.laps['Time'] > session.laps['Time'].quantile(0.66)]
    
    # Group by driver and find the best lap for each in Q3
    q3_best_laps = q3_laps.groupby('Driver')['LapTime'].min().sort_values().reset_index()
    q3_best_laps = q3_best_laps.head(10)  # Only keep the top 10

    fastest_lap_time = q3_best_laps.iloc[0]['LapTime']
    q3_best_laps['Gap'] = q3_best_laps['LapTime'] - fastest_lap_time
    q3_best_laps['Gap_seconds'] = q3_best_laps['Gap'].dt.total_seconds()
    q3_best_laps['LapTime_formatted'] = q3_best_laps['LapTime'].apply(format_lap_time)
    q3_best_laps['Position'] = range(1, len(q3_best_laps) + 1)

    # Merge with driver information
    drivers_info = session.results[['DriverNumber', 'Abbreviation', 'TeamName']].set_index('Abbreviation')
    q3_best_laps = q3_best_laps.join(drivers_info, on='Driver')

    return q3_best_laps

def get_team_colors(q3_best_laps):
    # Define colors for teams with a fallback color
    team_colors = {
        'Red Bull': '#00174C',  # Updated Red Bull color
        'Mercedes': '#00D2BE',
        'Ferrari': '#DC0000',
        'McLaren': '#FF8700',
        'Alpine': '#0090FF',
        'Aston Martin': '#006F62',
        'Williams': '#005AFF',
        'Alfa Romeo': '#900000',
        'AlphaTauri': '#2B4562',
        'Haas': '#B6BABD'
    }

    # Match team names to colors with a fallback to grey if the team isn't found
    colors = [team_colors.get(team, '#999999') for team in q3_best_laps['TeamName']]
    return colors

def create_static_plot(q3_best_laps, session_name, year):
    if q3_best_laps is None:
        print("No data to plot.")
        return

    drivers = q3_best_laps['Driver']
    gaps = q3_best_laps['Gap_seconds']
    lap_times = q3_best_laps['LapTime_formatted']
    team_colors = get_team_colors(q3_best_laps)

    plt.figure(figsize=(14, 8))
    bars = plt.barh(drivers, gaps, color=team_colors, edgecolor='black', height=0.5)

    # Adding the gap or lap time labels inside each bar
    for i, (bar, gap, lap_time, team) in enumerate(zip(bars, gaps, lap_times, q3_best_laps['TeamName'])):
        label_x_pos = bar.get_width() + 0.01 if i == 0 else bar.get_width() - 0.01
        label_text = lap_time if i == 0 else f'+{gap:.3f}s'
        label_ha = 'left' if i == 0 else 'right'
        label_color = 'black' if i == 0 else 'white'

        plt.text(label_x_pos,
                 bar.get_y() + bar.get_height() / 2,
                 label_text,
                 va='center', ha=label_ha, fontsize=12, color=label_color, weight='bold')

    # Adding position labels, driver numbers, and team names next to driver names
    for i, (pos, driver, num, team) in enumerate(zip(q3_best_laps['Position'], drivers, q3_best_laps['DriverNumber'], q3_best_laps['TeamName'])):
        plt.text(-0.1, i, f'P{pos} #{num} ({team})', va='center', ha='right', fontsize=12, color='black', weight='bold')

    # Customizing the plot
    plt.xlabel('Gap to Fastest (seconds)', fontsize=14)
    plt.title(f'{session_name} - Q3 Qualifying Gaps ({year})', fontsize=18, weight='bold')
    plt.gca().invert_yaxis()  # Invert y-axis to have the fastest on top
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Improved color contrast and spacing
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Adding subtle gradients to bars (optional)
    for bar in bars:
        bar.set_hatch('//')

    # Adding watermark
    font = font_manager.FontProperties(weight='bold', size=20)
    plt.text(0.95, 0.02, 'F1 DATA IQ', transform=plt.gcf().transFigure,
             fontsize=30, color='gray', alpha=0.5,
             ha='right', va='bottom', fontproperties=font)

    plt.tight_layout()
    name = f"{year}-{session_name}-Q-delta_to_pole.png"
    plt.savefig(name)

def create_image(year, gp):
    session_type = 'Q'  # Q for Qualifying

    session = load_session(year, gp, session_type)

    if session:
        q3_best_laps = process_q3_data(session)
        create_static_plot(q3_best_laps, session.event['EventName'], year)
    else:
        print("Session data could not be loaded.")

if __name__ == "__main__":
    create_image()
