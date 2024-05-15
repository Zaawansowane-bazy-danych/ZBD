import json
import asyncio
import requests
from requests.auth import HTTPBasicAuth
from tournament_generator import TournamentGenerator
from exceptions import NonexistentTournamentException
from models import Tournament
from exceptions import SurrealException


class SurrealHandler:

    def __init__(self):
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
            raise SurrealException(f'db error - code {req.status_code}')
        # print(req.json())
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
    result = res.get('result')[0]
    id, matches = result.get('id'), result.get('matches')
    if result is None:
        raise NonexistentTournamentException()
    return Tournament(id=id.replace('tournament:', ''), matches=matches)


'''
handler = SurrealHandler()
handler.update_tournament_score('b93c7ceb11cc11efaadf3c52824480ca', 0, 0, 'y', 130)
t = handler.update_tournament_score('b93c7ceb11cc11efaadf3c52824480ca', 0, 0, 'z', 20)
print(t)
print(type(t))
'''
