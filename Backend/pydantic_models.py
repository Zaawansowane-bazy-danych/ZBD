from pydantic.functional_validators import AfterValidator
from pydantic import BaseModel
from typing_extensions import Annotated


def check_duplicates(li: list[str]) -> list[str]:
    assert len(li) == len(set(li)), 'list contains duplicates'
    return li


def check_nonempty(li: list[str]) -> list[str]:
    assert len(li) > 0, 'empty list'
    return li


def check_positive(val: int | float) -> int | float:
    assert val >= 0, 'no negative values allowed'
    return val


class GenerationData(BaseModel):
    player_names: Annotated[list[str], AfterValidator(check_duplicates), AfterValidator(check_nonempty)]


class UpdateData(BaseModel):
    level: Annotated[int, AfterValidator(check_positive)]
    level_number: Annotated[int, AfterValidator(check_positive)]
    player_name: str
    score: Annotated[float, AfterValidator(check_positive)]
