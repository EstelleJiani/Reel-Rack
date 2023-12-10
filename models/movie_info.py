"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the MovieInfo class
"""

import datetime as dt

import api_info
import helpers


class MovieInfo:
    """
    The MovieInfo class
    """
    def __init__(
            self,
            movie_id: int,
            title: str = None,
            release_date: dt.date = None,
            overview: str = None,
            poster_path: str = None,
            poster_url: str = None
    ) -> None:
        """
        This is the MovieInfo class constructor
        """
        if not isinstance(movie_id, int):
            raise TypeError("'movie_id' must be an integer")
        if title is not None and \
           not isinstance(title, str):
            raise TypeError("'title' must be a string")
        if release_date is not None and \
           not isinstance(release_date, dt.date):
            raise TypeError("'release_date' must be a 'datetime.date' object")
        if overview is not None and \
           not isinstance(overview, str):
            raise TypeError("'overview' must be a string")
        if poster_path is not None and \
           not isinstance(poster_path, str):
            raise TypeError("'poster_path' must be a string")
        if poster_url is not None and \
           not isinstance(poster_url, str):
            raise TypeError("'poster_url' must be a string")

        if movie_id < 0:
            raise ValueError("'movie_id' must be larger than 0")

        self.movie_id = movie_id
        self.title = title
        self.release_date = release_date
        self.overview = overview
        self.poster_path = poster_path
        self.poster_url = poster_url

    def __str__(self) -> str:
        if isinstance(self.title, str) and \
           isinstance(self.release_date, dt.date):
            return f"{self.title} ({self.release_date.year})"
        return ""

    def fetch(self) -> None:
        """
        Fetch the movie data
        """
        movie_details_url = api_info.MOVIES_DETAILS_URL + str(self.movie_id)
        movie_detail = helpers.fetch_data_from_url(movie_details_url)
        if movie_detail == {}:
            return

        try:
            self.title = movie_detail["title"]
            self.release_date = helpers.string_to_date(
                movie_detail["release_date"]
            )
            self.overview = movie_detail["overview"]
            self.poster_path = movie_detail["poster_path"]
            self.poster_url = helpers.get_image_url(
                helpers.ImageType.POSTER,
                self.poster_path
            )
        except KeyError:
            self.title = None
            self.release_date = None
            self.overview = None
            self.poster_path = None
            self.poster_url = None
