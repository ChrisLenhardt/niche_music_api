from fastapi import FastAPI, Depends
from supabase import create_client
import os

app = FastAPI()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"]
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