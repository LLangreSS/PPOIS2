import pytest
from studio.people import Person, Director, Actor
from studio.exceptions import InvalidDataFormatError


def test_person_validation():
    p = Person("John")
    with pytest.raises(InvalidDataFormatError, match="Name cannot be empty"):
        p.name = ""

    with pytest.raises(InvalidDataFormatError, match="is_busy must be a boolean"):
        p.is_busy = "True"


def test_director_style_validation():
    d = Director("Nolan", "Sci-Fi")
    with pytest.raises(InvalidDataFormatError, match="Style cannot be empty"):
        d.style = ""


def test_actor_rank():
    a = Actor("Leo", "Star")
    assert a.rank == "Star"
    a.rank = "Legend"
    assert a.rank == "Legend"
