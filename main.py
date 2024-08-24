import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

def get_movie_recommendations(genres, favorite_movies):
 
    prompt = f"""
    You are a movie recommendation expert. Based on the user's favorite genres and top movies, provide personalized movie recommendations.

    User's favorite genres: {', '.join(genres)}
    User's top 3 favorite movies: {', '.join(favorite_movies)}

    For each recommended movie, provide a detailed summary that includes:
    - **Movie Name**: The title of the movie.
    - **Genre**: The genre of the movie.
    - **Subject**: A brief description of the movie's plot or main theme.

    Present the recommendations in a clear table format with the following columns:
    - **Movie Name**
    - **Genre**
    - **Subject**

    Ensure the recommendations are diverse and align well with the genres and movies provided.
    """
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a movie recommendation assistant. Recommend movies based on the user's favorite genres and movies."},
            {"role": "user", "content": prompt}
        ],
    )
    
    response = completion.choices[0].message.content
    return response.strip()


st.set_page_config(page_title='Movie Recommendation System', page_icon='🎬', layout='wide')

st.title('🎬 Movie Recommendation System')
st.markdown("""
Welcome to the Movie Recommendation System! 🎥🍿

This app helps you discover new movies based on your favorite genres and movies. Simply provide your top 3 favorite movies and select your preferred genres. Click on the button to get personalized movie recommendations.

### How to Run?
1. **🎯 Select Your Favorite Genres:** Choose the genres you love.
2. **🎬 Specify Your Top 3 Favorite Movies:** Enter your top 3 favorite movies.
3. **🚀 Submit the Information:** Click the 'Get Recommendations' button.
4. **✨ Receive Personalized Recommendations:** Get movie recommendations tailored just for you.
""")

# User input for genres
st.sidebar.header('Select Your Favorite Genres')
genres = st.sidebar.multiselect(
    'Choose one or more genres:',
    ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
)

# User input for favorite movies
st.sidebar.header('Top 3 Favorite Movies')
favorite_movies = []
for i in range(3):
    movie = st.sidebar.text_input(f'Favorite Movie #{i+1}', key=f'movie_{i}')
    if movie:
        favorite_movies.append(movie)

# Get recommendations when the button is pressed
if st.sidebar.button('Get Recommendations'):
    if genres and len(favorite_movies) == 3:
        recommendations = get_movie_recommendations(genres, favorite_movies)
        
        # Display the recommendations
        st.write("### Movie Recommendations")
        st.write(recommendations)
        
        # Optionally, you could parse and display this in a table format
        # For simplicity, we'll just show the raw text response
    else:
        st.error('Please select genres and enter your top 3 favorite movies.')