from fastapi import FastAPI, Request
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions import (
    SurrealException,
    NonexistentTournamentException,
    NonexistentPlayerException,
    NonexistentMatchException,
    IllegalScoringException,
)
from surreal_handler import SurrealHandler
from tournament_generator import TournamentGenerator
from models import Tournament
from pydantic_models import GenerationData, UpdateData

# uvicorn main:app --reload

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(ValidationError)
def unicorn_exception_handler(request: Request, e: ValidationError):
    return JSONResponse(
        status_code=422,
        content={'detail': 'Data validation error'},
    )


@app.exception_handler(NonexistentTournamentException)
def unicorn_exception_handler(request: Request, e: NonexistentTournamentException):
    return JSONResponse(
        status_code=404,
        content={'detail': 'Tournament does not exist'},
    )


@app.exception_handler(NonexistentMatchException)
def unicorn_exception_handler(request: Request, e: NonexistentMatchException):
    return JSONResponse(
        status_code=404,
        content={'detail': 'No such match found'},
    )


@app.exception_handler(NonexistentPlayerException)
def unicorn_exception_handler(request: Request, e: NonexistentPlayerException):
    return JSONResponse(
        status_code=404,
        content={'detail': str(e)},
    )


@app.exception_handler(IllegalScoringException)
def unicorn_exception_handler(request: Request, e: IllegalScoringException):
    return JSONResponse(
        status_code=422,
        content={'detail': str(e)},
    )


@app.exception_handler(SurrealException)
def unicorn_exception_handler(request: Request, e: SurrealException):
    return JSONResponse(
        status_code=422,
        content={'detail': str(e)},
    )


@app.get('/')
def root():
    return {'hello': 'world'}


@app.post('/tournament/', response_model=Tournament, status_code=201)
def generate_tournament(data: GenerationData):
    generator = TournamentGenerator(data.player_names)
    tournament = generator.construct_tournament()
    handler = SurrealHandler()
    handler.create_tournament(tournament)
    return tournament


@app.put('/tournament/{tournament_id}', response_model=Tournament, status_code=200)
def update_tournament(tournament_id: str, data: UpdateData):
    handler = SurrealHandler()
    tournament = handler.update_tournament_score(
        tournament_id,
        data.level,
        data.level_number,
        data.player_name,
        data.score)
    return tournament


@app.get('/tournament/{tournament_id}', response_model=Tournament, status_code=200)
def get_tournament(tournament_id: str):
    handler = SurrealHandler()
    tournament = handler.get_tournament(tournament_id)
    return tournament


@app.delete('/tournament/{tournament_id}', status_code=204)
def delete_tournament(tournament_id: str):
    handler = SurrealHandler()
    handler.delete_tournament(tournament_id)
    return JSONResponse(status_code=204)