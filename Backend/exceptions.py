class NonexistentPlayerException(Exception):
    def __init__(self, message='nonexistent player'):
        super().__init__(message)


class NonexistentMatchException(Exception):
    def __init__(self, message='nonexistent match'):
        super().__init__(message)


class NonexistentTournamentException(Exception):
    def __init__(self, message='nonexistent tournament'):
        super().__init__(message)


class SurrealException(Exception):
    def __init__(self, message='db error'):
        super().__init__(message)