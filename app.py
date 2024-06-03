import streamlit as st
import pandas as pd
import numpy as np

from movie_data import MovieData

movie_posters_path = 'https://image.tmdb.org/t/p/w500/'
data_path = 'data/movies_5-29-24.pkl'
movies = MovieData(data_path)

st.title('Movie Suggester')

if st.button('Pick a random movie'):
    random_movie = movies.get_random_movie()
    st.write(random_movie['title'])
    try:
        st.image(movie_posters_path + random_movie['poster_path'])
    except:
        pass

# Textbox for user to enter text for similarity search and a button
text = st.text_area('Type anything...')
if st.button('Find similar movies'):
    similar_movies, response = movies.get_similar_movies_rag(text)
    if similar_movies is not None:
        st.write(response)
        for i, movie in similar_movies.iterrows():
            st.write(movie['title'])
            try:
                st.image(movie_posters_path + movie['poster_path'])
            except:
                pass
    else:
        st.write('Something went wrong.')

# text = st.text_area('Type anything...')