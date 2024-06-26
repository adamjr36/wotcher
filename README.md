# Wotcher, Harry!

A movie recommendation system using streamlit for a simple UI, and LangChain, OpenAI, and Pinecone to create a RAG LLM model. 

## Usage
Go to [wotcher](https://wotcher.streamlit.app/), type anything you like into the textbox, and watch as you get movie recommendations based on real data.

## Data

Data pulled from [Kaggle](https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies/data) and downloaded as a CSV. Last updated 6/8/24.

1. Some data exploration and processing is done in movies-eda.ipynb
2. The result of that is embedded and uploaded to pinecone with process_new_movie_data.py
3. The MovieData class in movie_data.py contains functions to find similar movies given some query

The data really comes initially from TMDB and could come directly from there, but it was trivially easy to use the Kaggle dataset.

## What's Next (theoretically)

Ideally:
1. Process the user input with an LLM to generate a better query to match against the Pinecone data, and iterate on the current LLM prompt for post-processing.
2. Write a script to automate steps 1 and 2 from the Data section above, and schedule a job to download the new movie dataset every day and to upsert new/changed rows.
3. Get data directly from TMDB to have a more reliable data source with more features to do more in-depth data analysis
