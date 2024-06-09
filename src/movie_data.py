import pandas as pd

from langchain_pinecone import PineconeVectorStore  
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

# Load global script variables
from GLOBALS import llm_model, embedding_model, pinecone_index

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Variables
K = 10 # Num results from pinecone

# MovieData class
class MovieData:
    def __init__(self, data_path, k=3):
        # Initialize the data from csv
        self.data_path = data_path
        self.data = pd.read_pickle(data_path)
        self.n = len(self.data)
        self.k = k

        # Set column id as index
        self.data.set_index('id', inplace=True)

        # Setup emb and pinecone client
        embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = PineconeVectorStore(index_name=pinecone_index, embedding=embeddings)

        # RAG model
        llm = ChatOpenAI(model=llm_model)
        retriever = self.vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": K})
        prompt_template = PromptTemplate.from_template(prompt)
        prompt_template = prompt_template.partial(k=self.k, K=K)
        
        def format_pinecone_response(response):
            return "\n\n".join(resp.page_content for resp in response)
        
        self.rag = (
            {"context": retriever | format_pinecone_response, "query": RunnablePassthrough()}
            | prompt_template
            | llm
            | JsonOutputParser(pydantic_object=Response)
        )

    # Get a random movie - return a pd Series
    def get_random_movie(self):
        i = np.random.randint(self.n)
        return self.data.iloc[i]
    
    # Get k similar movies - return a pd DataFrame
    def get_similar_movies(self, query):
        similars = [ v.page_content for v in self.vectorstore.similarity_search(query, k=K) ]

        # Get the indices of the similar movies, where s in similars is like 'id: xxxx, ...'
        try:
            indices = [ int(s.split(',', 1)[0][4:]) for s in similars ]
            return self.data.loc[indices]
        except:
            return None
    
    # Get k similar movies - RAG model
    def get_similar_movies_rag(self, query):
        try:
            response = self.rag.invoke(query)

            ids = self.parse_ids(response['ids'])
            return self.data.loc[ids], response['response']
        except Exception as e:
            print(e) 
            return None, None
    
    # ids could be [id1, id2, id3] or '['id1,id2,id3']' - return a list of ints
    def parse_ids(self, ids):
        if not ids:
            return []
        if ids[0] == '[':
            return list(map(int, ids[1:-1].split(',')))
        else:
            return list(map(int, ids))



# PROMPT and OUTPUT FORMAT
prompt = """
### CONTEXT ####
You are an assistant for suggesting movies based on user queries. Use the following {K} retrieved movies as context to suggest up to {k} similar movies to the user. Use three sentences maximum in your response and keep the answer concise. Refer to movies by their title only. 

Retrieved Movies:
{context}

User Query: 
{query}

### OUTPUT FORMAT ###:
You must format your response as a valid JSON object as follows:
{{
    "ids": "[Int]", // Integer ids from the retrieved movies context
    "response": "" // Your string response, referring to the suggested movies by title
}}

Reponse:"""

class Response(BaseModel):
    ids: list[int] = None
    response: str = Field(description="The helpful LLM response to the user query")



# # If runnign script directly, create MovieData object and call get_similar_movies on every user input
# if __name__ == '__main__':
#     data_path = '../data/movies_5-29-24.pkl'
#     movies = MovieData(data_path)
#     while True:
#         text = input('Type anything...')
#         print(movies.get_similar_movies_rag(text))