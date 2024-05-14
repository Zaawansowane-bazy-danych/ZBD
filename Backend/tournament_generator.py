from player_handler import PlayerHandler
from models import Player, Match, Tournament
from math import log2


class TournamentGenerator:
    def __init__(self, names: list[str]):
        self.names = names
        self._player_handler = PlayerHandler(names)

    def construct_tournament(self) -> Tournament:
        players = self._player_handler.players
        n_levels = _find_num_of_levels(players)
        levels = [level := _generate_level(players, 0)]
        for i in range(1, n_levels):
            empty_players = [None for _ in range(len(level))]
            levels.append(level := _generate_level(empty_players, i))
        return Tournament(matches=levels)


def _find_num_of_levels(n: int | list) -> int:
    return int(log2(n)) if isinstance(n, int) else int(log2(len(n)))


def _generate_level(players: list[Player | None], level: int) -> list[Match]:
    matches = []
    it = iter(players)
    pairs = zip(it, it)
    for i, (x, y) in enumerate(pairs):
        matches.append(Match(x, y, level, i))
    return matches
