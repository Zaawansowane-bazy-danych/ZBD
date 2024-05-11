from dataclasses import dataclass


@dataclass
class Player:
    name: str

    def __str__(self):
        return f'Player {self.name}'


@dataclass
class Match:
    player_left: Player
    player_right: Player
    level: int
    score_left: float | None = None
    score_right: float | None = None
    winner: Player | None = None

    def __str__(self):
        return f'{self.player_left} vs {self.player_right}'

    def right_win(self):
        self.winner = self.player_right

    def left_win(self):
        self.winner = self.player_left

    def play_left(self, score: float):
        self.score_left = score

    def play_right(self, score: float):
        self.score_right = score

@dataclass
class Tournament:
    matches: list[list[Match]]

    def __str__(self):
        repr = ''
        for level in self.matches:
            for match in level:
                repr += str(match) + '\n'
            repr += '\n'
        return repr
