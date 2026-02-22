import os

from fastapi import FastAPI, Depends
from supabase import create_client
from dotenv import load_dotenv
import os

from util.spotify_helpers import get_artist_image
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000/",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

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


@app.get("/test/spotipy")
def test_spotipy(): 
    return get_artist_image()
