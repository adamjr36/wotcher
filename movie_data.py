import numpy as np
import pandas as pd
from langchain_pinecone import PineconeVectorStore  
from langchain_openai import OpenAIEmbeddings

# Get OpenAI and Pinecone APIs from .env file
from dotenv import load_dotenv
load_dotenv()

# GLOBALS
embedding_model = 'text-embedding-3-small'
pinecone_index = 'movies-small'
cols = ['id', 'title', 'genres', 'original_language', 'overview', 'budget', 'revenue', 'runtime', 'tagline', 'credits', 'keywords']


# MovieData class
class MovieData:

    # Initialize the data from csv
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(data_path)
        self.n = len(self.data)

        # Set column id as index
        self.data.set_index('id', inplace=True)

        # Setup emb and pinecone client
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = PineconeVectorStore(index_name=pinecone_index, embedding=self.embeddings)
    
    # Get a random movie - return a pd Series
    def get_random_movie(self):
        i = np.random.randint(self.n)
        return self.data.iloc[i]
    
    # Get k similar movies - return a pd DataFrame
    def get_similar_movies(self, query, k=5):
        similars = [ v.page_content for v in self.vectorstore.similarity_search(query, k=k) ]

        # Get the indices of the similar movies, where s in similars is like 'id: xxxx, ...'
        try:
            indices = [ int(s.split(',', 1)[0][4:]) for s in similars ]
            return self.data.loc[indices]
        except:
            return None