import os
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from interfaces.routes.users.auth_interface import auth_router
from interfaces.routes.users.users_interface import user_router
from interfaces.routes.users.area_interface import area_router
from interfaces.routes.trainings.training_interface import training_router
from interfaces.routes.trainings.assignment_interface import assignment_router
from interfaces.routes.evaluations.questionnaire_interface import questionnaire_router
from interfaces.routes.evaluations.questions_answer_interface import questions_router
from interfaces.routes.trainings.user_training_interface import user_training_router
from interfaces.routes.evaluations.result_interface import result_router


routes = [
    auth_router,
    user_router,
    area_router,
    training_router,
    assignment_router,
    questionnaire_router,
    questions_router,
    user_training_router,
    result_router
]

origins = [
    'http://localhost:3000'
]

app = FastAPI()

media_dir = Path("media")
media_dir.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for route in routes:
    app.include_router(route)