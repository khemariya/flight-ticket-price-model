import streamlit as st
import pickle
import numpy as np

# Load the trained model
loaded_model = pickle.load(open('C:/Users/khema/OneDrive/Desktop/python/EDAFE/flights/finalModel.py', 'rb'))

# Function to preprocess user inputs
def preprocess_input(data):
    # Extract day, month, and year from Date_of_Journey
    data['Date'] = int(data['Date_of_Journey'].split('/')[0])
    data['Month'] = int(data['Date_of_Journey'].split('/')[1])
    data['Year'] = int(data['Date_of_Journey'].split('/')[2])

    # Extract hours and minutes from Dep_Time
    data['Dep_Time_hrs'] = int(data['Dep_Time'].split(':')[0])
    data['Dep_Time_Mns'] = int(data['Dep_Time'].split(':')[1])

    # Extract hours and minutes from Arrival_Time
    data['Arrival_Time_hours'] = int(data['Arrival_Time'].split(':')[0])
    data['Arrival_Time_Minutes'] = int(data['Arrival_Time'].split(':')[1].split(' ')[0])

    # Extract hours and minutes from Duration
    duration_split = data['Duration'].split(' ')
    if len(duration_split) == 2:
        data['Duration_hrs'] = int(duration_split[0].replace('h', ''))
        data['Duration_Mins'] = int(duration_split[1].replace('m', ''))
    elif 'h' in duration_split[0]:
        data['Duration_hrs'] = int(duration_split[0].replace('h', ''))
        data['Duration_Mins'] = 0
    else:
        data['Duration_hrs'] = 0
        data['Duration_Mins'] = int(duration_split[0].replace('m', ''))

    # Map Total_Stops to numerical values
    stops_map = {'non-stop': 0, '1 stop': 1, '2 stop': 2, '3 stop': 3, '4 stop': 4}
    data['Total_Stops'] = stops_map[data['Total_Stops']]

    # OneHotEncoding for Airline
    airlines = ['Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways', 'Airline_Jet Airways Business',
                'Airline_Multiple carriers', 'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 
                'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy']
    airline_map = {airline: 0 for airline in airlines}
    airline_key = 'Airline_' + data['Airline']
    if airline_key in airline_map:
        airline_map[airline_key] = 1

    # OneHotEncoding for Source
    sources = ['Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai']
    source_map = {source: 0 for source in sources}
    source_key = 'Source_' + data['Source']
    if source_key in source_map:
        source_map[source_key] = 1

    # OneHotEncoding for Destination
    destinations = ['Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi']
    destination_map = {destination: 0 for destination in destinations}
    destination_key = 'Destination_' + data['Destination']
    if destination_key in destination_map:
        destination_map[destination_key] = 1

    # Combine all the processed data into a single array
    processed_data = [
        data['Total_Stops'], data['Date'], data['Month'], data['Year'], 
        data['Dep_Time_hrs'], data['Dep_Time_Mns'], data['Arrival_Time_hours'], 
        data['Arrival_Time_Minutes'], data['Duration_hrs'], data['Duration_Mins']
    ] + list(airline_map.values()) + list(source_map.values()) + list(destination_map.values())

    return np.array(processed_data).reshape(1, -1)

# Streamlit app
def main():
    st.title("Flight Price Prediction")
    st.write("Enter the flight details to predict the price:")

    # User inputs
    Date_of_Journey = st.text_input("Date of Journey (DD/MM/YYYY)", "01/03/2023")
    Airline = st.selectbox("Airline", ["Air India", "GoAir", "IndiGo", "Jet Airways", "Jet Airways Business", 
                                       "Multiple carriers", "Multiple carriers Premium economy", "SpiceJet", 
                                       "Trujet", "Vistara", "Vistara Premium economy"])
    Source = st.selectbox("Source", ["Chennai", "Delhi", "Kolkata", "Mumbai"])
    Destination = st.selectbox("Destination", ["Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"])
    Total_Stops = st.selectbox("Total Stops", ["non-stop", "1 stop", "2 stop", "3 stop", "4 stop"])
    Additional_Info = st.text_input("Additional Info (Not used in prediction)", "No info")
    Dep_Time = st.text_input("Departure Time (HH:MM)", "22:20")
    Arrival_Time = st.text_input("Arrival Time (HH:MM)", "01:10")
    Duration = st.text_input("Duration (Hh Mm)", "2h 50m")

    input_data = {
        'Date_of_Journey': Date_of_Journey,
        'Airline': Airline,
        'Source': Source,
        'Destination': Destination,
        'Total_Stops': Total_Stops,
        'Dep_Time': Dep_Time,
        'Arrival_Time': Arrival_Time,
        'Duration': Duration
    }

    if st.button("Predict"):
        processed_data = preprocess_input(input_data)
        prediction = loaded_model.predict(processed_data)
        st.write(f"The predicted flight price is: {prediction[0]:.2f}")

if __name__ == "__main__":
    main()
