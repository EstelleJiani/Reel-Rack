"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is test file for helpers
"""

import datetime as dt
from unittest.mock import patch, mock_open
import requests

import helpers

MOCK_FETCH_DATA = {
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


def test_helpers_fetch_data_from_url():
    """
    Test fetch_data_from_url
    """
    with patch("helpers.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_FETCH_DATA

        assert helpers.fetch_data_from_url(
            "https://api.themoviedb.org/3/movie/15121"
        )["id"] == 15121


def test_helpers_fetch_data_from_url_connection_error():
    """
    Test fetch_data_from_url
    """
    with patch("helpers.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        assert helpers.fetch_data_from_url(
            "https://api.themoviedb.org/3/movie/15121"
        ).get("id") is None


def test_helpers_fetch_data_from_url_bad_status_code():
    """
    Test fetch_data_from_url
    """
    with patch("helpers.requests.get") as mock_get:
        mock_get.return_value.status_code = 404

        assert helpers.fetch_data_from_url(
            "https://api.themoviedb.org/3/movie/15121"
        ).get("id") is None


def test_helpers_save_list_to_file():
    """
    Test save_list_to_file
    """
    m = mock_open()
    with patch("builtins.open", m):
        helpers.save_list_to_file(
            helpers.FileType.WATCHED,
            MOCK_WATCHED_DATA
        )

    m.assert_called_once_with(
        "database/watched.txt",
        'w',
        encoding="utf-8")
    handle = m()
    handle.write.assert_called_with(
        "575264|0|2023-12-04 00:38:29.591473\n"
    )


def test_helpers_append_data_to_file():
    """
    Test append_data_to_file
    """
    m = mock_open()
    with patch("builtins.open", m):
        helpers.append_data_to_file(
            helpers.FileType.FAVOURITES,
            "120467|2023-12-04 01:02:03.123321\n"
        )

    m.assert_called_once_with(
        "database/favourites.txt",
        'a',
        encoding="utf-8")
    handle = m()
    handle.write.assert_called_once_with(
        "120467|2023-12-04 01:02:03.123321\n"
    )


def test_helpers_read_list_from_file():
    """
    Test read_list_from_file
    """
    with patch(
        "builtins.open",
        mock_open(
            read_data="335977|2023-12-02 13:00:22.392722\n"
                      "346698|2023-12-02 13:01:20.945094\n"
                      "753342|2023-12-02 23:05:19.537008\n"
        )
    ):
        assert helpers.read_list_from_file(helpers.FileType.WATCHLIST) == \
            [
                "335977|2023-12-02 13:00:22.392722\n",
                "346698|2023-12-02 13:01:20.945094\n",
                "753342|2023-12-02 23:05:19.537008\n"
            ]


def test_helpers_parse_data():
    """
    Test parse_data
    """
    assert helpers.parse_data(
        [
            "872585|9|2023-12-02 13:00:49.183311\n",
            "15121|0|2023-12-04 00:38:18.598298\n",
            "575264|0|2023-12-04 00:38:29.591473\n"
        ]
    ) == [
        ["575264", "0", "2023-12-04 00:38:29.591473"],
        ["15121", "0", "2023-12-04 00:38:18.598298"],
        ["872585", "9", "2023-12-02 13:00:49.183311"]
    ]


def test_helpers_get_image_config():
    """
    Test get_image_config
    """
    assert helpers.get_image_config(helpers.ImageType.POSTER) == \
        (
            "https://image.tmdb.org/t/p/",
            "w185"
        )


def test_helpers_get_image_url():
    """
    Test get_image_url
    """
    with patch("helpers.get_image_config") as mock_data:
        mock_data.return_value = (
            "https://image.tmdb.org/t/p/",
            "w185"
        )

        assert helpers.get_image_url(
            helpers.ImageType.POSTER,
            "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
         ) == "https://image.tmdb.org/t/p/w185/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"


def test_helpers_string_to_date():
    """
    Test string_to_date
    """
    assert helpers.string_to_date("2023-12-04") == dt.date(2023, 12, 4)


def test_helpers_string_to_datetime():
    """
    Test string_to_date
    """
    assert helpers.string_to_datetime("2023-12-04 00:38:18.598298") == \
           dt.datetime(2023, 12, 4, 0, 38, 18, 598298)
