
import streamlit as st
import plotly.express as px
import folium
import pandas as pd
from streamlit_folium import st_folium

# # Caching function to load and merge data
@st.cache_data
def load_data():
    train_data = pd.read_csv("train.csv")
    test_data = pd.read_csv("test.csv")
    merged_data = pd.concat([train_data, test_data], axis=0)
    return merged_data

# Reading train and test data
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# Merging train and test data
merged_data = pd.concat([train_data, test_data], axis=0)

merged_data

# Convert data types
merged_data['Delivery_person_Age'] = pd.to_numeric(merged_data['Delivery_person_Age'], errors='coerce')
merged_data['Delivery_person_Ratings'] = pd.to_numeric(merged_data['Delivery_person_Ratings'], errors='coerce')

# Filtering options


st.title("Food Delivery Data Dashboard")

# Adding a sidebar filter for Delivery Ratings
st.sidebar.header("Filter Options")
selected_rating = st.sidebar.selectbox("Select Delivery Rating", merged_data['Delivery_person_Ratings'].unique())

# Filtering the merged data based on user selection
filtered_data = merged_data[merged_data['Delivery_person_Ratings'] == selected_rating]

# Updating the displayed table and charts with filtered data
st.subheader("Filtered Data:")
st.write(filtered_data.head())

# Filtering options
age_filter = st.sidebar.slider("Select Age Range", 18, 60, (20, 40))
rating_filter = st.sidebar.slider("Select Rating", 0.0, 5.0, (3.0, 5.0))

# Filtering the merged data
filtered_data = merged_data[
    (merged_data['Delivery_person_Age'] >= age_filter[0]) &
    (merged_data['Delivery_person_Age'] <= age_filter[1]) &
    (merged_data['Delivery_person_Ratings'] >= rating_filter[0]) &
    (merged_data['Delivery_person_Ratings'] <= rating_filter[1])
]

st.write("Filtered Data:", filtered_data)

st.write("Filtered Data:", filtered_data)





# Displaying initial table of data
st.subheader("Merged Data:")
st.write(merged_data.head())

# Streamlit: Plotting relationship between age and ratings
fig_age_ratings = px.scatter(merged_data, x='Delivery_person_Age', y='Delivery_person_Ratings', title='Age vs Ratings')
st.plotly_chart(fig_age_ratings, key='age_ratings')

fig_age_ratings

# Plotting pie chart of ratings vs time ordered
fig_ratings_time = px.pie(merged_data, names='Delivery_person_Ratings', title='Ratings vs Time Ordered')
st.plotly_chart(fig_ratings_time, key='ratings_time')

fig_ratings_time

# Displaying delivery locations map
st.subheader("Delivery Locations Map:")
m = folium.Map(location=[merged_data['Delivery_location_latitude'].mean(), merged_data['Delivery_location_longitude'].mean()], zoom_start=10)



# Adding markers for restaurant locations
for index, row in merged_data.iterrows():
    folium.Marker([row['Restaurant_latitude'], row['Restaurant_longitude']], popup=f"Restaurant {row['ID']}").add_to(m)


# Displaying delivery locations map

locations = merged_data[['Delivery_location_latitude', 'Delivery_location_longitude']].copy()
locations.columns = ['lat', 'lon']  
st.map(locations)  # Displaying map with the new DataFrame





