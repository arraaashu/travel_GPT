import streamlit as st
import openai
import requests

# Load API keys
OPENAI_API_KEY = '*******************************************************'
TRIPADVISOR_API_KEY = '*************************************************'

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Function to fetch data from TripAdvisor
def get_travel_info(location):
    url = "https://tripadvisor1.p.rapidapi.com/locations/search"
    querystring = {"query": location, "limit": "10", "offset": "0", "units": "km"}

    headers = {
        'x-rapidapi-host': "tripadvisor1.p.rapidapi.com",
        'x-rapidapi-key': TRIPADVISOR_API_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

# Function to get a response from OpenAI
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# Define a simple prompt to wrap around the user's query
def generate_prompt(query):
    return f"User query: {query}\nResponse:"

# Helper function to extract location from query
def extract_location_from_query(query):
    words = query.split()
    if words:
        return words[-1]
    return None

# Streamlit Interface
st.title("Travel Destination AI Agent")
st.write("Ask me about travel destinations!")

query = st.text_input("Enter your travel-related question:")

if query:
    try:
        # Generate a response from the AI
        prompt = generate_prompt(query)
        response = get_openai_response(prompt)
        
        # Extract location from the query
        location = extract_location_from_query(query)
        
        if location:
            travel_info = get_travel_info(location)
            st.write(travel_info)
        else:
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
