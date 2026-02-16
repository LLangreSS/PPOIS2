import pytest
from studio.movie_studio import MovieStudio
from studio.production import ProductionStatus
from studio.exceptions import (
    WorkflowOrderError,
    GenreMismatchError
)


@pytest.fixture
def studio():
    s = MovieStudio("Hollywood")
    s.hire_director("Director A", "Drama")
    s.hire_actor("Actor A", "Star")
    s.buy_camera("IMAX", "12K")
    s.build_set("Studio 1", True)
    return s


def test_casting_genre_mismatch(studio):
    m_idx = studio.create_script("Fast & Furious", "Action", 120)
    with pytest.raises(GenreMismatchError, match="does not match genre"):
        studio.perform_casting(m_idx, 0, [])


def test_casting_success(studio):
    m_idx = studio.create_script("The Whale", "Drama", 90)
    studio.perform_casting(m_idx, 0, [0])
    assert studio.movies[m_idx].status == ProductionStatus.CASTING_DONE


def test_workflow_order_errors(studio):
    m_idx = studio.create_script("Order Test", "Drama", 100)
    with pytest.raises(WorkflowOrderError, match="Casting must be done"):
        studio.start_filming(m_idx, 0, 0)

    studio.perform_casting(m_idx, 0, [])
    with pytest.raises(WorkflowOrderError, match="Filming must be finished"):
        studio.run_post_production(m_idx)


def test_full_cycle_and_release(studio):
    m_idx = studio.create_script("Final", "Drama", 50)
    studio.perform_casting(m_idx, 0, [0])
    studio.start_filming(m_idx, 0, 0)
    studio.run_post_production(m_idx)
    studio.release_movie(m_idx)
    assert studio.movies[m_idx].status == ProductionStatus.RELEASED
