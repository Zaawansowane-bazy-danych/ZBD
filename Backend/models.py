import random
from dataclasses import dataclass
from uuid import uuid1
from exceptions import NonexistentPlayerException, NonexistentMatchException, IllegalScoringException
from pydantic import BaseModel


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
        if self.winner is not None or self.player_right is None or self.player_left is None:
            raise IllegalScoringException('This match is already concluded')
        if self.player_right.name == name:
            if self.score_right is not None:
                raise IllegalScoringException(f'Score for player {name} is already {self.score_right}')
            else:
                self.score_right = score
        elif self.player_left.name == name:
            if self.score_left is not None:
                raise IllegalScoringException(f'Score for player {name} is already {self.score_left}')
            else:
                self.score_left = score
        else:
            raise NonexistentPlayerException(f'No player {name} in this match')
        if self.score_left is None or self.score_right is None:
            return
        if self.score_left < self.score_right:
            self.winner = self.player_left
        elif self.score_left > self.score_right:
            self.winner = self.player_right
        else:
            self.score_left = None
            self.score_right = None
            self.winner = None


class Tournament(BaseModel):
    matches: list[list[Match]]
    id: str = str(uuid1()).replace('-', '')

    def fix(self):
        self.id = str(uuid1()).replace('-', '') + str(random.randint(100, 999))
        for match in self.matches[0]:
            if match.player_right is None and match.player_left is not None:
                match.winner = match.player_left
            elif match.player_left is None and match.player_right is not None:
                match.winner = match.player_right
            else:
                continue
            if len(self.matches) == 1:
                continue
            if match.number % 2 == 0:
                self.matches[1][int(match.number/2)].player_left = match.winner
            else:
                self.matches[1][int(match.number / 2)].player_right = match.winner

    def update(self, level: int, number: int, player_name: str, score: float):
        if score <= 0:
            raise IllegalScoringException('Negative score')
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
