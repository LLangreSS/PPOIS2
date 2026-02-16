import pytest
from studio.resources import Camera, MovieSet
from studio.exceptions import InvalidDataFormatError


def test_camera_invalid_data():
    c = Camera("Sony")
    with pytest.raises(InvalidDataFormatError, match="Camera model cannot be empty"):
        c.model = ""


def test_movie_set_invalid_data():
    s = MovieSet("London", False)
    with pytest.raises(InvalidDataFormatError, match="Location name cannot be empty"):
        s.location = ""


def test_resource_busy_type():
    c = Camera("Sony")
    with pytest.raises(InvalidDataFormatError, match="Status must be a boolean"):
        c.is_busy = 1
