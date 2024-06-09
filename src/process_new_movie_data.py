'''
Expect .pkl file with movie data to be in data/ directory, path specified as command line argument.

Embeds movie data into Pinecone vector store, and writes file_path + '_min.pkl' with only the cols necessary for app.py.
'''
import pandas as pd
import numpy as np
import argparse
import time 

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

from GLOBALS import pinecone_index, \
    embedding_model, embedding_dim, embedding_cols

from dotenv import load_dotenv
load_dotenv()

# Variables
min_cols = ['id', 'title', 'poster_path']

# Prep data for embedding
def apply_stringify_data(row):
    s = []
    for col in embedding_cols:
        s.append('{}: {}'.format(col, row[col]))
    return ', '.join(s)


if __name__ == '__main__':
    print('Starting...')
    parser = argparse.ArgumentParser(description='Embed movie data into Pinecone vector store.')
    parser.add_argument('file_path', type=str, help='Path to .pkl file with movie data.')
    args = parser.parse_args()
    print('File path: {}'.format(args.file_path))

    try:
        # Load data
        data = pd.read_pickle(args.file_path)
        print('Data loaded.')

        # Load Pinecone client
        pc = Pinecone() 
        if pinecone_index in pc.list_indexes().names():
            pc.delete_index(pinecone_index)
        
        pc.create_index(pinecone_index, 
                        dimension=embedding_dim,
                        metric='cosine',
                        spec=ServerlessSpec(cloud='aws', region='us-east-1'))

        while not pc.describe_index(pinecone_index).status['ready']:
            time.sleep(1)
        print('Pinecone index ready.')
    
        # Embed data
        embeddings = OpenAIEmbeddings(model=embedding_model)
        vectorstore = PineconeVectorStore(index_name=pinecone_index, embedding=embeddings)   

        texts = data.apply(apply_stringify_data, axis=1)
        texts = texts.to_list()

        print('Adding texts to Pinecone...')
        vectorstore.add_texts(texts)
        print('Texts added to Pinecone.')

        # Write min data
        min_data = data[min_cols]
        min_data.to_pickle(args.file_path.replace('.pkl', '_min.pkl'))
        print('Min data written to {}.'.format(args.file_path.replace('.pkl', '_min.pkl')))
    
    except Exception as e:
        print('Error! ', e)