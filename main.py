import os

from fastapi import FastAPI, Depends
from supabase import create_client
from dotenv import load_dotenv
import os
import openai

app = FastAPI()

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SECRET")
)

openaiClient = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/album/search/{type}/{query}")
def find_album(type: str, query: str):
    """
    Find album from db, changes search column depending on type
    """
    if type == "id":
        if not query.isnumeric():
            return "Please give a numeric input for id search! Alternatively, use the /name/{query} endpoint!"
        
        column = "position"
        data = (
            supabase
            .table("albums")
            .select("*")
            .eq(column,query)
            .limit(100)
            .execute()
        )


        return data
    elif type == "name":
        column = "release_name"
        
        data = (
            supabase
            .table("albums")
            .select("*")
            .ilike(column,query)
            .limit(100)
            .execute()
        )
    
        return data

@app.get("/vector/similar_albums/{genreString}")
def similarAlbumFromGenres(genreString: str):
    
    checkIfRowExists = supabase.table("cached_embeddings").select("*").eq("genre_string", genreString).execute()
    embedding = []
    
    if checkIfRowExists.data == []:
        response = openai.embeddings.create(
            input=genreString,
            model="text-embedding-3-small"
        )
        
        embedding = response.data[0].embedding
        
        supabase.table("cached_embeddings").insert({"genre_string": genreString, "embeddings": embedding}).execute()
    else:
        embedding = checkIfRowExists.data[0]["embeddings"]

    
    
    data = (supabase.rpc('match_albums', {"query_embedding": embedding, "match_threshold": 0.50, "match_count": 10}).execute())
    
    return data
