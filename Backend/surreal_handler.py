import json
import asyncio
import requests
from requests.auth import HTTPBasicAuth
from tournament_generator import TournamentGenerator
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

    def create_tournament(self, tournament: Tournament):
        query = f"""CREATE tournament:{tournament.id} CONTENT
        {tournament.model_dump_json(indent=2, exclude={'id'})}"""
        self.query(query)

    def get_tournament(self, tournament_id):
        query = f'SELECT * FROM tournament:{tournament_id}'
        self.query(query)

    def delete_tournament(self, tournament_id):
        query = f'DELETE tournament:{tournament_id}'
        self.query(query)
