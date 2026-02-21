from fastapi import FastAPI, Depends
from supabase import create_client
import os

app = FastAPI()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"]
)

@app.get("/album/{uid}")
def process_data(uid: str):
    data = (
        supabase
        .table("dummy_table")
        .select("*")
        .eq("release_name",uid)
        .execute()
    )


    return data