llm_model = 'gpt-4o'
embedding_model = 'text-embedding-3-small'
embedding_dim = 1536
embedding_cols = ['id', 'title', 'genres', 'original_language', 'overview', 'popularity', 'production_companies', 'release_date', 'budget', 'revenue', 'runtime', 'tagline', 'vote_average', 'vote_count', 'credits', 'keywords', 'recommendations']
pinecone_index = 'movies'

posters_path = 'https://image.tmdb.org/t/p/w500/'