import streamlit as st
import pandas as pd
import numpy as np

from movie_data import MovieData

movie_posters_path = 'https://image.tmdb.org/t/p/w500/'
data_path = 'data/movies_5-29-24.pkl'
movies = MovieData(data_path)

st.title('Wotcher, Harry!')
st.subheader('User the textbox below to describe what you want, and I will magically suggest the best possible movies.', divider='rainbow')


# Textbox for user to enter text for similarity search and a button
st.caption('Like it says below, type anything! Ask for specific actors, directors, genres, or plot points. You can ask for movies similar to other ones, or you can even describe the plot of a movie that doesn\'t exist! Feel free to expose your innermost secrets. If you don\'t like what I suggest, just type something else!')
text = st.text_area('Type anything...')

if st.button('Find similar movies'):
    with st.spinner('Magicking...'):
        similar_movies, response = movies.get_similar_movies_rag(text)
    st.balloons()
    if similar_movies is not None:
        st.write(response)

        titles = []
        posters = []
        for i, movie in similar_movies.iterrows():
            titles.append(movie['title'])
            posters.append(movie['poster_path'])

        cols = st.columns(len(titles))
        for i, col in enumerate(cols):
            with col:
                st.write(titles[i])
                try:
                    st.image(movie_posters_path + posters[i])
                except:
                    pass
    else:
        st.write('Something went wrong.')
