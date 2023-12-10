"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is test file for MovieInfo class.
"""

import datetime as dt
from unittest.mock import patch
import pytest

from models.movie_info import MovieInfo

MOCK_FETCH_DATA = {
    "id": 15121,
    "overview":
        "In the years before the Second World War, a tomboyish postulant "
        "at an Austrian abbey is hired as a governess in the home of a "
        "widowed naval captain with seven children, and brings a new love "
        "of life and music into the home.",
    "poster_path": "/5qQTu2iGTiQ2UvyGp0beQAZ2rKx.jpg",
    "release_date": "1965-03-29",
    "TITLE": "The Sound of Music"
}


@pytest.fixture(name="movie_info")
def movie_info_fixture():
    """
    Create an object for the test.
    """
    return MovieInfo(872585)


def test_movie_info_init():
    """
    Test the MovieInfo constructor.
    """
    movie_info = MovieInfo(
        15121,
        "The Sound of Music",
        dt.date(1965, 3, 29),
        "In the years before the Second World War",
        "/5qQTu2iGTiQ2UvyGp0beQAZ2rKx.jpg",
        ""
    )
    assert movie_info.movie_id == 15121
    assert isinstance(movie_info.movie_id, int)
    assert movie_info.title == "The Sound of Music"
    assert isinstance(movie_info.title, str)
    assert movie_info.release_date == dt.date(1965, 3, 29)
    assert isinstance(movie_info.release_date, dt.date)
    assert movie_info.overview == "In the years before the Second World War"
    assert isinstance(movie_info.overview, str)
    assert movie_info.poster_path == "/5qQTu2iGTiQ2UvyGp0beQAZ2rKx.jpg"
    assert isinstance(movie_info.poster_path, str)
    assert movie_info.poster_url == ""
    assert isinstance(movie_info.poster_url, str)


def test_movie_info_init_only_movie_id():
    """
    Test the MovieInfo constructor.
    """
    movie_info = MovieInfo(872585)
    assert movie_info.movie_id == 872585
    assert isinstance(movie_info.movie_id, int)


def test_movie_info_init_movie_id_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo('872585')
    assert "'movie_id' must be an integer" in str(excinfo.value)


def test_movie_info_init_title_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo(872585, ["Oppenheimer"])
    assert "'title' must be a string" in str(excinfo.value)


def test_movie_info_init_release_date_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo(872585, release_date="2023-07-19")
    assert "'release_date' must be a 'datetime.date' object" in \
        str(excinfo.value)


def test_movie_info_init_overview_date_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo(
            872585,
            overview=(
                "The story of J. Robert Oppenheimer's",
                "role in the development"
            )
        )
    assert "'overview' must be a string" in str(excinfo.value)


def test_movie_info_init_poster_path_date_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo(872585, poster_path=123)
    assert "'poster_path' must be a string" in str(excinfo.value)


def test_movie_info_init_poster_url_date_type_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieInfo(872585, poster_url=[""])
    assert "'poster_url' must be a string" in str(excinfo.value)


def test_movie_info_init_movie_id_value_error():
    """
    Test the MovieInfo constructor.
    """
    with pytest.raises(ValueError) as excinfo:
        MovieInfo(-872585)
    assert "'movie_id' must be larger than 0" in str(excinfo.value)


def test_movie_info_str():
    """
    Test the MovieInfo str method
    """
    movie_info = MovieInfo(15121)
    movie_info.title = "The Sound of Music"
    movie_info.release_date = dt.date(1965, 3, 29)
    assert str(movie_info) == "The Sound of Music (1965)"


def test_movie_info_str_only_movie_id(movie_info):
    """
    Test the MovieInfo str method
    """
    assert str(movie_info) == ""


def test_movie_info_fetch(movie_info):
    """
    Test the fetch method.
    """
    movie_info.fetch()
    assert movie_info.movie_id == 872585
    assert movie_info.title == "Oppenheimer"
    assert movie_info.release_date == dt.date(2023, 7, 19)
    assert movie_info.overview == \
        "The story of J. Robert Oppenheimer's role in the development "\
        "of the atomic bomb during World War II."
    assert movie_info.poster_path == "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
    assert movie_info.poster_url == \
        "https://image.tmdb.org/t/p/w185/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"


def test_movie_info_fetch_resource_not_found():
    """
    Test the fetch method
    """
    movie_info = MovieInfo(0)
    movie_info.fetch()
    assert movie_info.title is None
    assert movie_info.release_date is None
    assert movie_info.overview is None
    assert movie_info.poster_path is None
    assert movie_info.poster_url is None


def test_movie_info_fetch_resource_with_wrong_key():
    """
    Test the fetch method
    """
    with patch("models.movie_info.helpers.fetch_data_from_url") as mock_func:
        mock_func.return_value = MOCK_FETCH_DATA

        movie_info = MovieInfo(15121)
        movie_info.fetch()
        assert movie_info.title is None
        assert movie_info.release_date is None
        assert movie_info.overview is None
        assert movie_info.poster_path is None
        assert movie_info.poster_url is None
