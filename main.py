from fastapi import FastAPI, Depends
from supabase import create_client
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

@app.get("/album/search_id/{uid}")
def find_album_by_id(uid: str):
    """
    Find album from db, takes position uid
    """
    column = "position"
    try:
        int(uid)
    except:
        return "Please input a numerical value!"
    data = (
        supabase
        .table("albums")
        .select("*")
        .eq(column,uid)
        .limit(100)
        .execute()
    )


    return data

@app.get("/album/search_name/{release_name}")
def find_album_by_name(release_name: str):
    """
    Find album from db, takes release name
    """
    column = "release_name"

    data = (
        supabase
        .table("albums")
        .select("*")
        .ilike(column,release_name)
        .limit(100)
        .execute()
    )
    
    return data