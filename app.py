import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Download the data
data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text('Loading data...done!')

st.write('Done! (using st.cache)')

# Checkbox to show the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Histogram of the pickups by hour
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# GeoMap with the lat lon of pickups
st.subheader('Map of all pickups by hour')
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.text(f'Pickups at {hour_to_filter}:00')
st.map(filtered_data)
