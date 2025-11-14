import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from interfaces.routes.users.auth_interface import auth_router
from interfaces.routes.users.users_interface import user_router
from interfaces.routes.users.area_interface import area_router
from interfaces.routes.trainings.training_interface import training_router
from interfaces.routes.trainings.assignment_interface import assignment_router


routes = [
    auth_router,
    user_router,
    area_router,
    training_router,
    assignment_router
]

origins = [
    '*'
]

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


for route in routes:
    app.include_router(route)