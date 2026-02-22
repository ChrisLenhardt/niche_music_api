import os

from fastapi import FastAPI, Depends
from supabase import create_client
from dotenv import load_dotenv
import os

from util.spotify_helpers import get_artist_image
from fastapi.middleware.cors import CORSMiddleware

import openai
import musicbrainzngs
import requests

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

musicbrainzngs.set_useragent("niche.ai", "1.0.0", "zerubbabelashenafi@gmail.com")

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
        try:
            response = openai.embeddings.create(
                input=genreString,
                model="text-embedding-3-small"
            )
            
            embedding = response.data[0].embedding
            
            supabase.table("cached_embeddings").insert({"genre_string": genreString, "embeddings": embedding}).execute()
        except:
            return "Error Occured creating embeddings"
    else:
        embedding = checkIfRowExists.data[0]["embeddings"]

    
    
    data = (supabase.rpc('match_albums', {"query_embedding": embedding, "match_threshold": 0.50, "match_count": 10}).execute())
    
    return data

@app.get("/musicbrainz/search/{artist}/{release}")
def searchForCoverArt(artist: str, release: str):
    try:
        # release_group = musicbrainzngs.search_release_groups(artist=artist, release=release, strict=True)
        url=f"https://musicbrainz.org/ws/2/release-group/?query=artist:{artist}ANDrelease:{release}&fmt=json"
        response = requests.get(url, timeout=5.0)
        release_group = {}
        if response.status_code == 200:
            release_group = response.json()
        
    except:
        return "Error Occurred1"
    release_id=0
    
    if release_group != {}:
        try:
            release_id = release_group["release-groups"][0]["id"]
            print(release_id)
        except:
            return "Error Occurred2"
        
        
        # for release in release_list:
        #     if "status" in release:
        #         if release["status"] == "Official":
        #             release_id = release["id"]
        #             break
        
        try:
            getImageURL = f"https://coverartarchive.org/release-group/{release_id}"
            print(getImageURL)
            imageResponse = requests.get(getImageURL, timeout=5.0, allow_redirects=True)
            followThrough = requests.get(imageResponse.url, timeout=5.0)
            
            image_list = followThrough.json()
            print(image_list)
                
        except:
            return "Error occurred fetching image list"
        
        try:
            image_url = image_list["images"][0]["image"]
            return image_url
        except:
            return "Error Occurred3"
    
    return "Nothing found!"

@app.get("/musicbrainz/search/{artist}")
def genreStringFromArtist(artist: str):
    try:
        artist = musicbrainzngs.search_artists(artist=artist)
    except:
        return "Error occured fetching artist"
        
    try:
        artist_genres = artist["artist-list"][0]["tag-list"]
    except:
        return "Error occured getting genres"
    sorted_genres = sorted(artist_genres, key=lambda d: d["count"], reverse=True)
    genreString = ""
    for i in range(3):
        if i > len(sorted_genres) - 1:
            break
        else:
            genreString += sorted_genres[i]["name"]
        if i != 2:
            genreString += ", "
    
    return genreString


@app.get("/test/spotipy")
def test_spotipy(): 
    return get_artist_image()
