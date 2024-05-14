from fastapi import FastAPI
from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, ValidationError
from pydantic.functional_validators import AfterValidator

from surreal_handler import SurrealHandler
from tournament_generator import TournamentGenerator
from models import Tournament

# uvicorn main:app --reload

app = FastAPI()


def check_duplicates(l: list[str]) -> list[str]:
    assert len(l) == len(set(l)), 'list contains duplicates'
    return l


class GenerationData(BaseModel):
    player_names: Annotated[list[str], AfterValidator(check_duplicates)]


class UpdateData(BaseModel):
    tournament_id: str
    level: int
    level_number: int
    player_name: str
    score: float


@app.get('/')
def root():
    return {'hello': 'world'}


@app.post('/generate/')
def generate_tournament(data: GenerationData):
    generator = TournamentGenerator(data.player_names)
    tournament = generator.construct_tournament()
    handler = SurrealHandler()
    handler.create_tournament(tournament)
    return tournament


@app.post('/update-tournament/')    # roboczy endpoint poki nie ma pisania do bazy
def update_t(data: Tournament):
    return data


@app.post('/update/')               # też roboczy na razie
def update_tournament(data: UpdateData):
    tournament = None
    # TODO: DOWNLOAD FROM THE DATABASE
    tournament.update(data.level, data.level_number, data.player_name, data.score)
    # TODO: SAVE TO THE DATABASE
    return tournament
