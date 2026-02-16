import pytest
from studio.production import Script, Movie, ProductionStatus
from studio.exceptions import NoneObjectError


def test_movie_init_none_script():
    with pytest.raises(NoneObjectError, match="must be initialized with a Script"):
        Movie(None)


def test_movie_properties():
    s = Script("Title", "Genre", 100)
    m = Movie(s)
    assert m.status == ProductionStatus.PLANNED
    m.status = ProductionStatus.SCRIPT_READY
    assert m.status == ProductionStatus.SCRIPT_READY
