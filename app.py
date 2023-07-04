import pandas as pd
import streamlit as st

# Function to process the data
def process_data(df):
    # Convert 'lastsvcdate' and 'nextsvcdate' columns to datetime
    df['lastsvcdate'] = pd.to_datetime(df['lastsvcdate'])
    df['nextsvcdate'] = pd.to_datetime(df['nextsvcdate'])
    df['scheduledate'] = pd.to_datetime(df['scheduledate'])

    data = df[['address1','accountid','customername','lastsvcdate', 'nextsvcdate', 'scheduledate', 'eventname']]

    data['date_difference'] = data['nextsvcdate'] - data['scheduledate']

    max_day_diff = {
        'All-Natural Barrier Spray': 14,
        'Synthetic Barrier Spray': 21,
        'Botanical Barrier 3 Week': 21,
        'Accelerated Service 1': 7,
        'Barrier + Tick Service': 21  # No maximum day difference specified
    }

    data['day_difference'] = data.apply(
        lambda row: max_day_diff[row['eventname']] - row['date_difference'].days,
        axis=1
    )

    sorted_data = data.sort_values(by='day_difference', ascending=False)
    return sorted_data

# Function to convert timedelta values to strings
def convert_timedelta_to_string(td):
    return str(td)

# Streamlit app
def main():
    # Page configuration
    st.set_page_config(page_title='CSV Analyzer', layout='wide')

    # Title and file upload
    st.title('CSV Analyzer')
    uploaded_file = st.file_uploader('Upload a CSV file', type='csv')

    if uploaded_file is not None:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)

        # Process the data
        sorted_data = process_data(df)

        # Convert timedelta values to strings
        sorted_data['date_difference'] = sorted_data['date_difference'].apply(convert_timedelta_to_string)

        # Display the tables
        st.subheader('Too Short')
        st.dataframe(sorted_data[sorted_data['day_difference'] > 0])

        st.subheader('Too Long')
        st.dataframe(sorted_data[sorted_data['day_difference'] < 0])

# Run the app
if __name__ == '__main__':
    main()
