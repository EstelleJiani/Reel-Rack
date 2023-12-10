"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is test file for Movie class.
"""

import datetime as dt
from unittest.mock import patch
import pytest

import helpers
from models.movie import Movie, WatchStatus
from models.movie_info import MovieInfo

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
MOCK_DATETIME_DATA = dt.datetime(2023, 12, 4, 1, 2, 3, 123321)


@pytest.fixture(name="movie")
def movie_fixture():
    """
    Create an object for the test.
    """
    return Movie(MovieInfo(872585))


def test_movie_init():
    """
    Test the Movie constructor.
    """
    movie = Movie(
        MovieInfo(15121),
        WatchStatus.RATED,
        dt.datetime(2023, 12, 4, 1, 2, 3, 123321),
        10,
        True
    )
    assert movie.movie_info.movie_id == 15121
    assert isinstance(movie.movie_info.movie_id, int)
    assert movie.watch_status == WatchStatus.RATED
    assert isinstance(movie.watch_status, WatchStatus)
    assert movie.action_datetime == dt.datetime(2023, 12, 4, 1, 2, 3, 123321)
    assert isinstance(movie.action_datetime, dt.datetime)
    assert movie.rating_score == 10
    assert isinstance(movie.rating_score, int)
    assert movie.is_favourite is True
    assert isinstance(movie.is_favourite, bool)


def test_movie_init_only_movie_id(movie):
    """
    Test the Movie constructor.
    """
    assert movie.movie_info.movie_id == 872585
    assert isinstance(movie.movie_info.movie_id, int)


def test_movie_init_movie_info_type_error():
    """
    Test the Movie constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        Movie(15121)
    assert "'movie_info' must be a 'MovieInfo' object" in str(excinfo.value)


def test_movie_init_watch_status_type_error():
    """
    Test the Movie constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        Movie(MovieInfo(15121), 0)
    assert "'watch_status' must be a 'WatchStatus' enum" in str(excinfo.value)


def test_movie_init_action_datetime_type_error():
    """
    Test the Movie constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        Movie(MovieInfo(15121), action_datetime=dt.date(2023, 12, 4))
    assert "'action_datetime' must be a 'datetime.datetime' object" in \
        str(excinfo.value)


def test_movie_init_rating_score_type_error():
    """
    Test the Movie constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        Movie(MovieInfo(15121), rating_score='10')
    assert "'rating_score' must be an integer" in str(excinfo.value)


def test_movie_init_is_favourite_type_error():
    """
    Test the Movie constructor.
    """
    with pytest.raises(TypeError) as excinfo:
        Movie(MovieInfo(15121), is_favourite=1)
    assert "'is_favourite' must be a boolean" in str(excinfo.value)


def test_movie_str(movie):
    """
    Test the Movie str method.
    """
    movie.movie_info.title = "Oppenheimer"
    movie.movie_info.release_date = dt.date(2023, 7, 19)
    assert str(movie) == "Oppenheimer (2023)"


def test_movie_str_only_movie_id(movie):
    """
    Test the Movie str method.
    """
    assert str(movie) == ""


def test_movie_load_movie_details(movie):
    """
    Test the load movie details method.
    """
    movie.load_movie_details()
    assert movie.movie_info.movie_id == 872585
    assert movie.movie_info.title == "Oppenheimer"
    assert movie.movie_info.release_date == dt.date(2023, 7, 19)
    assert movie.movie_info.overview == \
        "The story of J. Robert Oppenheimer's role in the development "\
        "of the atomic bomb during World War II."
    assert movie.movie_info.poster_path == "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
    assert movie.movie_info.poster_url == \
        "https://image.tmdb.org/t/p/w185/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"


def test_movie_load_watch_status():
    """
    Test the load watch status
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.side_effect = [
            MOCK_WATCHLIST_DATA,
            MOCK_WATCHED_DATA
        ]

        movie = Movie(MovieInfo(120467))
        movie.load_watch_status()
        assert movie.watch_status == WatchStatus.DEFAULT


def test_movie_load_watch_status_watchlist():
    """
    Test the load watch status
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.side_effect = [
            MOCK_WATCHLIST_DATA,
            MOCK_WATCHED_DATA
        ]

        movie = Movie(MovieInfo(346698))
        movie.load_watch_status()
        assert movie.watch_status == WatchStatus.WATCHLIST


def test_movie_load_watch_status_watched():
    """
    Test the load watch status
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.side_effect = [
            MOCK_WATCHLIST_DATA,
            MOCK_WATCHED_DATA
        ]

        movie = Movie(MovieInfo(15121))
        movie.load_watch_status()
        assert movie.watch_status == WatchStatus.WATCHED


def test_movie_load_watch_status_rated(movie):
    """
    Test the load watch status
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.side_effect = [
            MOCK_WATCHLIST_DATA,
            MOCK_WATCHED_DATA
        ]

        movie.load_watch_status()
        assert movie.watch_status == WatchStatus.RATED


def test_movie_set_rating_score():
    """
    Test the set_rating_score method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_WATCHED_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(15121))
        movie.set_rating_score(10)
        mock_save.assert_called_once_with(
            helpers.FileType.WATCHED,
            [
                "872585|9|2023-12-02 13:00:49.183311\n",
                "575264|0|2023-12-04 00:38:29.591473\n",
                "15121|10|2023-12-04 01:02:03.123321\n"
            ]
        )


def test_movie_set_rating_score_type_error(movie):
    """
    Test the set_rating_score method of the Movie class
    """
    with pytest.raises(TypeError) as excinfo:
        movie.set_rating_score('8')
    assert "'score' must be an integer" in str(excinfo.value)


def test_movie_set_rating_score_value_error(movie):
    """
    Test the set_rating_score method of the Movie class
    """
    with pytest.raises(ValueError) as excinfo:
        movie.set_rating_score(11)
    assert "'score' must be between 1 and 10" in str(excinfo.value)


def test_movie_remove_rating_score():
    """
    Test the remove_rating_score method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_WATCHED_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(15121))
        movie.remove_rating_score()
        mock_save.assert_called_once_with(
            helpers.FileType.WATCHED,
            [
                "872585|9|2023-12-02 13:00:49.183311\n",
                "575264|0|2023-12-04 00:38:29.591473\n",
                "15121|0|2023-12-04 01:02:03.123321\n"
            ]
        )


def test_movie_load_favourite_status_true():
    """
    Test the load_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        movie = Movie(MovieInfo(15121))
        movie.load_favourite_status()
        assert movie.is_favourite is True


def test_movie_load_favourite_status_false(movie):
    """
    Test the load_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        movie.load_favourite_status()
        assert movie.is_favourite is False


def test_movie_get_favourite_status_true():
    """
    Test the get_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        movie = Movie(MovieInfo(15121))
        assert movie.get_favourite_status() is True


def test_movie_get_favourite_status_false(movie):
    """
    Test the get_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_func:
        mock_func.return_value = MOCK_FAVOURITES_DATA

        assert movie.get_favourite_status() is False


def test_movie_set_favourite_status_true(movie):
    """
    Test the set_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.append_data_to_file") as mock_append, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie.set_favourite_status(True)
        mock_append.assert_called_once_with(
            helpers.FileType.FAVOURITES,
            "872585|2023-12-04 01:02:03.123321\n"
        )


def test_movie_set_favourite_status_false():
    """
    Test the set_favourite_status method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_FAVOURITES_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(15121))
        movie.set_favourite_status(False)
        mock_save.assert_called_once_with(
            helpers.FileType.FAVOURITES,
            []
        )


def test_movie_add_to_favourites(movie):
    """
    Test the add_to_favourites method of the Movie class
    """
    with patch("models.movie.helpers.append_data_to_file") as mock_append, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie.add_to_favourites()
        mock_append.assert_called_once_with(
            helpers.FileType.FAVOURITES,
            "872585|2023-12-04 01:02:03.123321\n"
        )


def test_movie_remove_from_favourites():
    """
    Test the remove_from_favourites method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_FAVOURITES_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(15121))
        movie.remove_from_favourites()
        mock_save.assert_called_once_with(
            helpers.FileType.FAVOURITES,
            []
        )


def test_movie_add_to_watched_list(movie):
    """
    Test the add_to_watched_list method of the Movie class
    """
    with patch("models.movie.helpers.append_data_to_file") as mock_append, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie.add_to_watched_list()
        mock_append.assert_called_once_with(
            helpers.FileType.WATCHED,
            "872585|0|2023-12-04 01:02:03.123321\n"
        )


def test_movie_remove_from_watched_list(movie):
    """
    Test the remove_from_watched_list method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_WATCHED_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie.remove_from_watched_list()
        mock_save.assert_called_once_with(
            helpers.FileType.WATCHED,
            [
                "15121|0|2023-12-04 00:38:18.598298\n",
                "575264|0|2023-12-04 00:38:29.591473\n"
            ]
        )


def test_movie_add_to_watchlist(movie):
    """
    Test the add_to_watchlist method of the Movie class
    """
    with patch("models.movie.helpers.append_data_to_file") as mock_append, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie.add_to_watchlist()
        mock_append.assert_called_once_with(
            helpers.FileType.WATCHLIST,
            "872585|2023-12-04 01:02:03.123321\n"
        )


def test_movie_remove_from_watchlist():
    """
    Test the remove_from_watchlist method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_WATCHLIST_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(335977))
        movie.remove_from_watchlist()
        mock_save.assert_called_once_with(
            helpers.FileType.WATCHLIST,
            [
                "346698|2023-12-02 13:01:20.945094\n",
                "753342|2023-12-02 23:05:19.537008\n"
            ]
        )


def test_movie_remove_movie_from_list():
    """
    Test the remove_movie_from_list method of the Movie class
    """
    with patch("models.movie.helpers.read_list_from_file") as mock_read, \
         patch("models.movie.helpers.save_list_to_file") as mock_save, \
         patch("models.movie.dt.datetime") as mock_datetime:
        mock_read.return_value = MOCK_WATCHLIST_DATA
        mock_datetime.now.return_value = MOCK_DATETIME_DATA

        movie = Movie(MovieInfo(335977))
        movie.remove_movie_from_list(helpers.FileType.WATCHLIST)
        mock_save.assert_called_once_with(
            helpers.FileType.WATCHLIST,
            [
                "346698|2023-12-02 13:01:20.945094\n",
                "753342|2023-12-02 23:05:19.537008\n"
            ]
        )
