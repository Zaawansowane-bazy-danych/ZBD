import json
import requests
import os
from requests.auth import HTTPBasicAuth
from exceptions import NonexistentTournamentException
from models import Tournament
from exceptions import SurrealException


class SurrealHandler:

    def __init__(self):
        self.url = os.environ.get('SURREALDB_URL')
        self.login = os.environ.get('SUERREALDB_LOGIN')
        self.password = os.environ.get('SUERREALDB_PASSWORD')
        self.ns = os.environ.get('SUERREALDB_NS')
        self.db = os.environ.get('SUERREALDB_DB')
        if None in [self.url, self.login, self.password, self.ns, self.db]:
            raise SurrealException('Failed to retrieve database access data from the server environment')

    def __init__json__(self):
        with open('config.json') as f:
            config = json.load(f)
            self.url = config.get('link')
            self.login = config.get('login')
            self.password = config.get('password')
            self.ns = config.get('ns')
            self.db = config.get('db')

    def query(self, query):
        req = requests.post(
            self.url,
            headers={
                'Accept': 'application/json',
                'ns': self.ns,
                'db': self.db,
            },
            data=query,
            auth=HTTPBasicAuth(self.login, self.password))
        if req.status_code != 200:
            raise SurrealException(f'Database error - surrealdb server response code {req.status_code}')
        return req.json()

    def create_tournament(self, tournament: Tournament):
        query = f"""CREATE tournament:{tournament.id} CONTENT
        {tournament.model_dump_json(indent=2, exclude={'id'})}"""
        self.query(query)

    def get_tournament(self, tournament_id: str):
        query = f'SELECT * FROM tournament:{tournament_id}'
        response = self.query(query)
        return _parse_response(response)

    def delete_tournament(self, tournament_id: str):
        query = f'DELETE tournament:{tournament_id}'
        self.query(query)

    def update_tournament_score(self, tournament_id: str, level: int, number: int, player_name: str, score: float):
        tournament = self.get_tournament(tournament_id)
        tournament.update(level, number, player_name, score)
        matches_json = tournament.model_dump_json(indent=2, exclude={'id'}).replace('{\n  "matches": ', '').removesuffix('\n}')
        query = f'UPDATE tournament:{tournament_id} SET matches = {matches_json}'
        response = self.query(query)
        return _parse_response(response)


def _parse_response(response):
    res = response[0] if type(response) == list else response
    if res.get('result') in [None, []]:
        raise NonexistentTournamentException()
    result = res.get('result')[0]
    id, matches = result.get('id'), result.get('matches')
    if result is None:
        raise NonexistentTournamentException()
    return Tournament(id=id.replace('tournament:', ''), matches=matches)
