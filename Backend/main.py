from fastapi import FastAPI
from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel, ValidationError
from pydantic.functional_validators import AfterValidator
from tournament_generator import TournamentGenerator

# uvicorn main:app --reload

app = FastAPI()


def check_duplicates(l: list[str]) -> list[str]:
    assert len(l) == len(set(l)), 'list contains duplicates'
    return l


class TournamentData(BaseModel):
    player_names: Annotated[list[str], AfterValidator(check_duplicates)]


@app.get('/')
def root():
    return {'hello': 'world'}


@app.post('/generate/')
def generate_tournament(data: TournamentData):
    generator = TournamentGenerator(data.player_names)
    tournament = generator.construct_tournament()
    return tournament
