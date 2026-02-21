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

@app.get("/album/{uid}")
def find_album(uid: str):
    """
    Find album from db, can take position uid or album name
    """
    column = "position"
    try:
        int(uid)
    except:
        column = "release_name"
    data = (
        supabase
        .table("albums")
        .select("*")
        .eq(column,uid)
        .execute()
    )


    return data