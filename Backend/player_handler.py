from models import Player
from random import shuffle


class PlayerHandler:
    players: list[Player]

    def __init__(self, names: list[str]):
        self.players = _generate_players(names)


def _generate_players(names: list[str]) -> list[Player]:
    players = [Player(n) for n in names]
    shuffle(players)
    size = _find_smallest_size(names)
    players = _extend_list_nones(players, size)
    print(players)
    return players


def _find_smallest_size(n: int | list) -> int:
    size = 2
    num = n if isinstance(n, int) else len(n)
    while size < num:
        size *= 2
    return size


def _extend_list_nones(players: list[Player | None], size: int) -> list[Player | None]:
    if size < len(players):
        return players
    nones = size - len(players)
    for n in range(nones):
        players.insert(2*n, None)
    players.reverse()
    return players
