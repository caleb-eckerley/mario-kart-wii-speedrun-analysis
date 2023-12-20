import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/speedrun_data')

#print(df['items'].unique())
#print(df['character'].unique())
#print(df['vehicle'].unique())

other_df = df.replace(['Bullet Bike', 'Sneakster', 'Dolphin Dasher', 'Tiny Titan', 'Quacker', 'Magikruiser', 'Standard Bike S', 'Standard Kart S', 'Booster Seat'], 'Other')
other_df = other_df.replace(['Baby Daisy', 'Bowser Jr.', 'Rosalina', 'Yoshi', 'Bowser', 'Dry Bowser', 'Toadette', 'Luigi', 'Mii', 'Mario', 'Toad', 'Dry Bones', 'Waluigi'], 'Other')

vehicle_frequency = px.histogram(df, x='vehicle', title='Vehicle Frequency', text_auto='.2s')
vehicle_frequency.update_layout(font=dict(size=20))
#vehicle_frequency.show()

character_frequency = px.histogram(df, x='character', title='Character Frequency', text_auto='.2s')
character_frequency.update_layout(font=dict(size=20))
#character_frequency.show()

vehicle_frequency_other = px.histogram(other_df, x='vehicle', title='Vehicle Frequency')
vehicle_frequency_other.update_layout(font=dict(size=20))
#vehicle_frequency_other.show()

character_frequency_other = px.histogram(other_df, x='character', title='Character Frequency')
#character_frequency_other.show()

vehicle_times_h = px.histogram(
  other_df,
  x='time',
  color='vehicle',
  marginal='rug',
  title='Histogram of Times Across Vehicles'
)
vehicle_times_h.update_layout(font=dict(size=20))
#vehicle_times_h.show()

character_times_h = px.histogram(other_df, x='time', color='character', marginal='rug', title='Histogram of Times Across Characters')
character_times_h.update_layout(font=dict(size=20))
character_times_h.show()