from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



routes = [
    
]

origins = [
    '*'
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


for route in routes:
    app.include_router(route)