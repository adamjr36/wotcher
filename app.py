import streamlit as st
import pandas as pd
import numpy as np

movie_posters_path = 'https://image.tmdb.org/t/p/w500/'
data_path = 'data/movies_5-29-24.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(data_path)
    return data

df = load_data()
n = len(df)
st.title('Movie Suggester')

if st.button('Pick a random movie'):
    i = np.random.randint(n)
    random_movie = df.iloc[i]
    st.write(random_movie['title'])
    try:
        st.image(movie_posters_path + random_movie['poster_path'])
    except:
        pass

# text = st.text_area('Type anything...')