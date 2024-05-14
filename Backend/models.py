from dataclasses import dataclass
from uuid import uuid1
from exceptions import NonexistentPlayerException, NonexistentMatchException
from pydantic import BaseModel

@dataclass
class Player:
    name: str

    def __str__(self):
        return f'Player {self.name}'


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
        return f'{self.player_left} vs {self.player_right}'

    def update_score(self, name: str, score: float):
        if self.player_right.name == name:
            self.score_right = score
        elif self.player_left.name == name:
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

    def __post_init__(self):
        self.id = str(uuid1())

    def update(self, level: int, number: int, player_name: str, score: float):
        for match in self.matches[level]:
            if match.number == number:
                match.update_score(player_name, score)
                break
        else:
            raise NonexistentMatchException()

    def __str__(self):
        repr = ''
        for level in self.matches:
            for match in level:
                repr += str(match) + '\n'
            repr += '\n'
        return repr
