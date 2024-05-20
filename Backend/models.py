from dataclasses import dataclass
from uuid import uuid1
from exceptions import NonexistentPlayerException, NonexistentMatchException
from pydantic import BaseModel, field_validator


@dataclass
class Player:
    name: str

    def __str__(self):
        return self.name


@dataclass
class Match:
    player_left: Player | None
    player_right: Player | None
    level: int
    number: int
    score_left: float | None = None
    score_right: float | None = None
    winner: Player | None = None

    def __str__(self):
        return f'{self.player_left} ({self.score_left}) vs {self.player_right} ({self.score_right})'

    def update_score(self, name: str, score: float):
        if self.player_right is not None and self.player_right.name == name:
            self.score_right = score
        elif self.player_left is not None and self.player_left.name == name:
            self.score_left = score
        else:
            raise NonexistentPlayerException(f'player {name} does not exist')
        if self.score_left is None or self.score_right is None:
            return
        if self.score_left > self.score_right:
            self.winner = self.player_left
        else:
            self.winner = self.player_right


class Tournament(BaseModel):
    matches: list[list[Match]]
    id: str = str(uuid1()).replace('-', '')

    @field_validator('matches', ...)
    def __pydantic_post_init__(self):
        # self.id = 'id'
        for match in self.matches[0]:
            match.winner = match.player_left
            if match.player_right is None and match.player_left is not None:
                match.winner = match.player_left
            elif match.player_left is None and match.player_right is not None:
                match.winner = match.player_right

    def update(self, level: int, number: int, player_name: str, score: float):
        try:
            self.matches[level][number].update_score(player_name, score)
            winner = self.matches[level][number].winner
            if winner is not None and level + 1 < len(self.matches):
                index = int(number/2)
                if number % 2 == 0:
                    self.matches[level + 1][index].player_left = winner
                else:
                    self.matches[level + 1][index].player_right = winner
        except IndexError:
            raise NonexistentMatchException()

    def __str__(self):
        repr = ''
        for level in self.matches:
            for match in level:
                repr += str(match) + '\n'
            repr += '\n'
        return repr
