import streamlit as st
import pandas as pd
import os

from GLOBALS import posters_path

from movie_data import MovieData

# root directory
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_path = os.path.join(root, 'data/movies_6-8-24_min.pkl')
movies = MovieData(data_path)

st.set_page_config(
    page_title='Wotcher, Harry!',
    page_icon='🧙🏼‍♂️',
    layout='centered',
    initial_sidebar_state='auto'
)

st.logo(os.path.join(root, 'assets/wotcher.png'), link='https://img.buzzfeed.com/buzzfeed-static/static/2021-04/9/0/asset/4b34c94ad75b/sub-buzz-3314-1617926736-5.png')
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
        st.divider()
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
                    st.image(posters_path + posters[i])
                except:
                    pass
    else:
        st.write('Something went wrong.')
