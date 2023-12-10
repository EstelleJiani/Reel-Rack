"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is test file for MovieList class.
"""

import datetime as dt
from unittest.mock import patch
import pytest

import helpers
from models.movie import Movie
from models.movie_info import MovieInfo
from models.movie_list import MovieList

MOCK_FETCH_IMAGE_CONFIG_DATA = {
    "images": {
        "secure_base_url": "https://image.tmdb.org/t/p/",
        "poster_sizes": [
            "w92",
            "w154",
            "w185",
            "w342",
            "w500",
            "w780",
            "original"
        ]
    }
}
MOCK_FETCH_DATA = {
    "page": 1,
    "results": [
        {
            "id": 872585,
            "overview": "The story of J. Robert Oppenheimer's",
            "poster_path": "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
            "release_date": "2023-07-19",
            "title": "Oppenheimer"
        },
        {
            "id": 753342,
            "overview": "An epic that details the checkered",
            "poster_path": "/jE5o7y9K6pZtWNNMEw3IdpHuncR.jpg",
            "release_date": "2023-11-22",
            "title": "Napoleon"
        },
        {
            "id": 1075794,
            "overview": "Jaded 74-year-old lizard Leo has been",
            "poster_path": "/pD6sL4vntUOXHmuvJPPZAgvyfd9.jpg",
            "release_date": "2023-11-17",
            "title": "Leo"
        },
        {
            "id": 507089,
            "overview": "Recently fired and desperate for work",
            "poster_path": "/j9mH1pr3IahtraTWxVEMANmPSGR.jpg",
            "release_date": "2023-10-25",
            "title": "Five Nights at Freddy's"
        }
    ],
    'total_pages': 1000,
    'total_results': 20000
}
MOCK_WRONG_KEY_DATA = {
    "id": 15121,
    "overview":
        "In the years before the Second World War, a tomboyish postulant "
        "at an Austrian abbey is hired as a governess in the home of a "
        "widowed naval captain with seven children, and brings a new love "
        "of life and music into the home.",
    "poster_path": "/5qQTu2iGTiQ2UvyGp0beQAZ2rKx.jpg",
    "release_date": "1965-03-29",
    "title": "The Sound of Music"
}

MOCK_FAVOURITES_DATA = [
    "15121|2023-12-04 00:40:06.161434\n"
]
MOCK_WATCHED_DATA = [
    "872585|9|2023-12-02 13:00:49.183311\n",
    "15121|0|2023-12-04 00:38:18.598298\n",
    "575264|0|2023-12-04 00:38:29.591473\n"
]
MOCK_WATCHLIST_DATA = [
    "335977|2023-12-02 13:00:22.392722\n",
    "346698|2023-12-02 13:01:20.945094\n",
    "753342|2023-12-02 23:05:19.537008\n"
]


@pytest.fixture(name="movie_list")
def movie_list_fixture():
    """
    Create an object for test.
    """
    movies = [
        Movie(MovieInfo(391713)),
        Movie(MovieInfo(331482)),
        Movie(MovieInfo(7980))
    ]
    return MovieList(movies)


def test_movie_list_init(movie_list):
    """
    Test the MovieList constructor.
    """
    assert movie_list.movies[0].movie_info.movie_id == 391713
    assert movie_list.movies[1].movie_info.movie_id == 331482
    assert movie_list.movies[2].movie_info.movie_id == 7980
    assert isinstance(movie_list.movies, list)


def test_movie_list_init_type_error():
    """
    Test the MovieList constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        MovieList(Movie(MovieInfo(15121)))
    assert "'movies' must be a list" in str(excinfo.value)


def test_movie_list_len(movie_list):
    """
    Test the movie_list length method.
    """
    assert len(movie_list) == 3


def test_movie_list_len_with_no_items():
    """
    Test the movie_list length method.
    """
    movie_list = MovieList()
    assert len(movie_list) == 0


def test_movie_list_len_movies_is_none():
    """
    Test the movie_list length method.
    """
    movie_list = MovieList()
    movie_list.movies = None
    assert len(movie_list) == 0


def test_movie_list_getitem(movie_list):
    """
    Test the movie_list getitem method.
    """
    assert movie_list[1].movie_info.movie_id == 331482


def test_movie_list_getitem_with_no_items():
    """
    Test the movie_list getitem method.
    """
    movie_list = MovieList()
    assert movie_list[0] is None


def test_movie_list_parse_movies_data(movie_list):
    """
    Test the parse_movies_data method.
    """
    movies = movie_list.parse_movies_data(MOCK_FETCH_DATA)
    assert movies[0].movie_info.movie_id == 872585
    assert movies[1].movie_info.movie_id == 753342
    assert movies[2].movie_info.movie_id == 1075794
    assert movies[3].movie_info.movie_id == 507089


def test_movie_list_parse_movies_data_with_no_items(movie_list):
    """
    Test the parse_movies_data method.
    """
    assert movie_list.parse_movies_data({}) == []


def test_movie_list_parse_movies_data_with_wrong_key(movie_list):
    """
    Test the parse_movies_data method.
    """
    assert movie_list.parse_movies_data(MOCK_WRONG_KEY_DATA) == []


def test_movie_list_fetch_trending_movies_day(movie_list):
    """
    Test the fetch_trending_movies method with the parameter being 'day'.
    """
    with patch("models.movie_list.helpers.fetch_data_from_url") as mock_func:
        mock_func.side_effect = [
            MOCK_FETCH_DATA,
            MOCK_FETCH_IMAGE_CONFIG_DATA
        ]

        movie_list.fetch_trending_movies("day")
        assert movie_list.movies[0].movie_info.movie_id == 872585
        assert movie_list.movies[1].movie_info.movie_id == 753342
        assert movie_list.movies[2].movie_info.movie_id == 1075794
        assert movie_list.movies[3].movie_info.movie_id == 507089


def test_movie_list_fetch_trending_movies_week(movie_list):
    """
    Test the fetch_trending_movies method with the parameter being 'week'.
    """
    with patch("models.movie_list.helpers.fetch_data_from_url") as mock_func:
        mock_func.side_effect = [
            MOCK_FETCH_DATA,
            MOCK_FETCH_IMAGE_CONFIG_DATA
        ]

        movie_list.fetch_trending_movies("week")
        assert movie_list.movies[0].movie_info.movie_id == 872585
        assert movie_list.movies[1].movie_info.movie_id == 753342
        assert movie_list.movies[2].movie_info.movie_id == 1075794
        assert movie_list.movies[3].movie_info.movie_id == 507089


def test_movie_list_fetch_trending_movies_type_error(movie_list):
    """
    Test the fetch_trending_movies method
    """
    with pytest.raises(ValueError) as excinfo:
        movie_list.fetch_trending_movies(1)
    assert "'time_window' must be 'day' or 'week'" in str(excinfo.value)


def test_movie_list_fetch_movies_from_search(movie_list):
    """
    Test the fetch_movies_from_search method.
    """
    movie_list.fetch_movies_from_search("The Grand Budapest Hotel")
    assert movie_list.movies[0].movie_info.movie_id == 120467
    assert movie_list.movies[0].movie_info.title == \
        "The Grand Budapest Hotel"
    assert movie_list.movies[0].movie_info.release_date == \
        dt.date(2014, 2, 26)
    assert movie_list.movies[0].movie_info.overview == \
        "The Grand Budapest Hotel tells of a legendary concierge at a famous "\
        "European hotel between the wars and his friendship with a young "\
        "employee who becomes his trusted protégé. The story involves the "\
        "theft and recovery of a priceless Renaissance painting, the battle "\
        "for an enormous family fortune and the slow and then sudden "\
        "upheavals that transformed Europe during the first half of the "\
        "20th century."
    assert movie_list.movies[0].movie_info.poster_path == \
        "/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg"
    assert movie_list.movies[0].movie_info.poster_url == \
        "https://image.tmdb.org/t/p/w185/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg"

    assert movie_list.movies[1].movie_info.movie_id == 1104269
    assert movie_list.movies[1].movie_info.title == \
        "The Making of The Grand Budapest Hotel"
    assert movie_list.movies[1].movie_info.release_date == \
        dt.date(2014, 6, 17)
    assert movie_list.movies[1].movie_info.overview == \
        "Behind the scenes featurette of making 'The Grand Budapest Hotel'"\
        " from the Criterion Collection release."
    assert movie_list.movies[1].movie_info.poster_path == \
        "/chlDOrJh8axzcTKctsZA8zOSVgo.jpg"
    assert movie_list.movies[1].movie_info.poster_url == \
        "https://image.tmdb.org/t/p/w185/chlDOrJh8axzcTKctsZA8zOSVgo.jpg"


def test_movie_list_fetch_movies_from_search_type_error(movie_list):
    """
    Test the fetch_movies_from_search method.
    """
    with pytest.raises(TypeError) as excinfo:
        movie_list.fetch_movies_from_search(15121)
    assert "'title' must be string" in str(excinfo.value)


def test_movie_list_load_favourites():
    """
    Test the load_favourites method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        movie_list = MovieList()
        movie_list.load_favourites()
        assert len(movie_list) == 1
        assert movie_list.movies[0].movie_info.movie_id == 15121


def test_movie_list_load_favourites_file_not_found():
    """
    Test the load_favourites method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = []

        movie_list = MovieList()
        movie_list.load_favourites()
        assert len(movie_list) == 0


def test_movie_list_load_watched_list():
    """
    Test the load_watched_list method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_WATCHED_DATA

        movie_list = MovieList()
        movie_list.load_watched_list()
        assert len(movie_list) == 3
        assert movie_list.movies[0].movie_info.movie_id == 575264
        assert movie_list.movies[1].movie_info.movie_id == 15121
        assert movie_list.movies[2].movie_info.movie_id == 872585


def test_movie_list_load_watched_list_file_not_found():
    """
    Test the load_watched_list method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = []

        movie_list = MovieList()
        movie_list.load_watched_list()
        assert len(movie_list) == 0


def test_movie_list_load_watchlist():
    """
    Test the load_watchlist method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_WATCHLIST_DATA

        movie_list = MovieList()
        movie_list.load_watchlist()
        assert len(movie_list) == 3
        assert movie_list.movies[0].movie_info.movie_id == 753342
        assert movie_list.movies[1].movie_info.movie_id == 346698
        assert movie_list.movies[2].movie_info.movie_id == 335977


def test_movie_list_load_watchlist_file_not_found():
    """
    Test the load_watchlist method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = []

        movie_list = MovieList()
        movie_list.load_watchlist()
        assert len(movie_list) == 0


def test_movie_list_load_movies_from_file():
    """
    Test the load_movies_from_file method of the MovieList class
    """
    with patch("models.movie_list.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        movie_list = MovieList()
        movie_list.load_movies_from_file(helpers.FileType.FAVOURITES)
        assert len(movie_list) == 1
        assert movie_list.movies[0].movie_info.movie_id == 15121


def test_movie_list_load_movies_from_file_type_error(movie_list):
    """
    Test the load_movies_from_file method of the MovieList class
    """
    with pytest.raises(TypeError) as excinfo:
        movie_list.load_movies_from_file("database/favourites.txt")
    assert "'file_type' must be a 'FileType' enum" in str(excinfo.value)
