"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the MovieList class
"""

from typing_extensions import Literal, TypeAlias

import api_info
import helpers
from models.movie import Movie
from models.movie_info import MovieInfo

TIME_WINDOW: TypeAlias = Literal["day", "week"]
VALID_TIME_WINDOWS = ("day", "week")


class MovieList:
    """
    List of movie model
    """
    def __init__(self, movies: list[Movie] = None) -> None:
        """
        The MovieList class constructor
        """
        if movies is not None and \
           not isinstance(movies, list):
            raise TypeError("'movies' must be a list")

        if movies is None:
            movies = []
        self.movies = movies

    def __len__(self) -> int:
        if isinstance(self.movies, list):
            return len(self.movies)
        else:
            return 0

    def __getitem__(self, index) -> Movie:
        if isinstance(self.movies, list) and \
           len(self.movies) > 0:
            return self.movies[index]
        return None

    def parse_movies_data(self, data) -> list[Movie]:
        """
        Parse movies data
        """
        movies = []

        if data == {} or data is None:
            return movies

        try:
            for result in data["results"]:
                movie_info = \
                    MovieInfo(
                        int(result["id"]),
                        result["title"],
                        helpers.string_to_date(
                            result["release_date"]
                            ),
                        result["overview"],
                        result["poster_path"],
                        helpers.get_image_url(
                            helpers.ImageType.POSTER,
                            result["poster_path"]
                        )
                    )
                movies.append(Movie(movie_info))
        except KeyError:
            movies = []

        return movies

    def fetch_trending_movies(
            self,
            time_window: TIME_WINDOW = "day"
    ) -> None:
        """
        Get the trending movies by day/week
        """
        if time_window not in VALID_TIME_WINDOWS:
            raise ValueError("'time_window' must be 'day' or 'week'")

        results = helpers.fetch_data_from_url(
            api_info.TRENDING_MOVIES + time_window
        )

        self.movies = self.parse_movies_data(results)

    def fetch_movies_from_search(self, title: str) -> None:
        """
        Search movies by movie title
        """
        if not isinstance(title, str):
            raise TypeError("'title' must be string")

        results = helpers.fetch_data_from_url(
            api_info.SEARCH_MOVIE_URL,
            {"query": title}
        )
        self.movies = self.parse_movies_data(results)

    def load_favourites(self) -> None:
        """
        Load favourites from the favourites file
        """
        self.load_movies_from_file(helpers.FileType.FAVOURITES)

    def load_watched_list(self) -> None:
        """
        Load watched list from the watched file
        """
        self.load_movies_from_file(helpers.FileType.WATCHED)

    def load_watchlist(self) -> None:
        """
        Load watchlist from the watchlist file
        """
        self.load_movies_from_file(helpers.FileType.WATCHLIST)

    def load_movies_from_file(self, file_type: helpers.FileType) -> None:
        """
        Load movies from a file
        """
        if not isinstance(file_type, helpers.FileType):
            raise TypeError("'file_type' must be a 'FileType' enum")

        movies = \
            helpers.parse_data(
                helpers.read_list_from_file(file_type)
            )
        for movie in movies:
            self.movies.append(Movie(MovieInfo(int(movie[0]))))
