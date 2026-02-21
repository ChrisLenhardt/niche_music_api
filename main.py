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
        
