import streamlit as st
import pandas as pd
import pickle
from geopy.distance import geodesic
import folium
import google.generativeai as genai

# Load your pre-trained KMeans model
with open('kmeans_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load your restaurant data
df = pd.read_csv('Restaurant_data.csv')  # Replace with your actual dataset path

# Set up the Gemini model with the correct API key
api_key = "AIzaSyBQYNdW_uJ3sDAmF7zAYd3JgSWNbDB5410" 
genai.configure(api_key=api_key)
chef_model = genai.GenerativeModel("gemini-1.5-flash")

# Define the role of the assistant (Chef Assistant)
role_description = """You are a chef assistant chatbot. 
You help users with cooking-related questions, provide recipes, suggest meal ideas, offer cooking tips, 
and answer any other culinary-related queries. Always provide helpful, friendly, and detailed advice related to food, cooking, and recipes."""

# Streamlit app title and navigation
st.set_page_config(page_title="Zomato & Chef Assistant", page_icon=":robot_face:")
st.title("Zomato Restaurants and Chef Assistant")

# Create a sidebar for navigation between the tabs
tabs = ["Restaurant Recommendations", "Chef Assistant"]
selected_tab = st.sidebar.radio("Choose Tab", tabs)

# --- Tab 1: Restaurant Recommendations ---
if selected_tab == "Restaurant Recommendations":
    st.subheader("Restaurant Recommendations")

    # Sidebar for user inputs for restaurant recommendations
    st.sidebar.header("Recommendations")

    # 1. City selection
    city = st.sidebar.selectbox("Select City", df['City'].unique())

    # 2. Cuisine selection
    cuisines = st.sidebar.multiselect("Choose Cuisines", df['Cuisines'])

    # 3. User location input
    user_lat = st.sidebar.number_input("Enter Latitude")  # Default: Delhi
    user_lon = st.sidebar.number_input("Enter Longitude")  # Default: Delhi

    # 4. Radius for recommendations
    max_distance = st.sidebar.slider("Show restaurants within (km):", min_value=1, max_value=50, value=10)

    # Filter restaurants by city
    filtered_df = df[df['City'] == city]

    # Filter by selected cuisines
    if cuisines:
        filtered_df = filtered_df[filtered_df['Cuisines'].str.contains('|'.join(cuisines), case=False, na=False)]

    # Add distance from the user to the restaurants
    def calculate_distance(user_coords, restaurant_coords):
        return geodesic(user_coords, restaurant_coords).km

    filtered_df['Distance'] = filtered_df.apply(
        lambda row: calculate_distance((user_lat, user_lon), (row['Latitude'], row['Longitude'])),
        axis=1
    )

    # Filter by max distance
    filtered_df = filtered_df[filtered_df['Distance'] <= max_distance]

    # Display restaurants visually
    if not filtered_df.empty:
        st.subheader(f"Recommended Restaurants in {city} within {max_distance} km")
        for _, row in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])

                with col1:
                    # Check if the 'Cuisine Image URL' is missing (NaN), and replace with a placeholder image
                    st.image(row['Cuisine Image URL'] if pd.notna(row['Cuisine Image URL']) else 'https://via.placeholder.com/150', width=150)

                with col2:
                    st.markdown(f"**{row['Restaurant name']}**")
                    st.markdown(f"*Ratings:* {row['Ratings']}")
                    st.markdown(f"*Average Cost for Two:* ₹{row['Average cost for two']}")
                    st.markdown(f"*Price Range:* {row['Price range']}")
                    st.markdown(f"*Online Delivery:* {'Yes' if row['Online delivery'] else 'No'}")
                    st.markdown(f"*Table Booking:* {'Yes' if row['Table booking'] else 'No'}")
                    st.markdown(f"*Distance:* {row['Distance']:.2f} km")
                    st.markdown("---")
    else:
        st.write("No restaurants found")

    # Display restaurants on a map
    if not filtered_df.empty:
        st.subheader("Map View")
        map_center = [user_lat, user_lon]
        folium_map = folium.Map(location=map_center, zoom_start=12)

        folium.Marker(location=[user_lat, user_lon], popup="Your Location", icon=folium.Icon(color='blue')).add_to(folium_map)

        for _, row in filtered_df.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"{row['Restaurant name']} ({row['Cuisines']})",
                icon=folium.Icon(color='green')
            ).add_to(folium_map)

        st.components.v1.html(folium_map._repr_html_(), height=500)

# --- Tab 2: Chef Assistant Chatbot ---
elif selected_tab == "Chef Assistant":
    st.subheader("Chef Assistant Chatbot")

    # Start a chat with the model, including the history with a greeting
    chat = chef_model.start_chat(
        history=[
            {"role": "user", "parts": ["Hello, Chef!"]},
            {"role": "model", "parts": ["Hello! I'm your Chef Assistant. How can I assist you with cooking today?"]},
            {"role": "model", "parts": [role_description]},  # Include the role description for the assistant
        ]
    )

    # Streamlit UI for user input
    user_input = st.text_input("Ask me anything about cooking:")

    if user_input:
        # Send the user message to the chat model and get the response
        response = chat.send_message(user_input)
        st.write(f"Assistant: {response.text}")
