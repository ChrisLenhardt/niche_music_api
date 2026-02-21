The backend has the purpose of processing advanced table queries

User story: I want to find top N album recommendations based on genre similarity to 1) searched genre or 2) example album

Requirements:
* Connections to supabase
* Publish usable API
* Encode genre names as vector encodings to calculate vector similarity

Setting up the env:
* Install fastapi (you may find it useful to create a python env if conda is already installed)

```
pip install "fastapi[standard]"
```

* to start project run:
```
export SUPABASE_URL=*insert_url_here*
export SUPABASE_SERVICE_ROLE_KEY=*insert_key_here*
fastapi dev main.py
```
