"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the Movie class
"""

import datetime as dt
from enum import Enum

import helpers
from models.movie_info import MovieInfo


class WatchStatus(Enum):
    """
    The WatchStatus class.
    Enum class defining the types of watch status.
    """
    DEFAULT = 0
    WATCHLIST = 1
    WATCHED = 2
    RATED = 3


class Movie:
    """
    The Movie class
    """
    def __init__(
            self,
            movie_info: MovieInfo,
            watch_status: WatchStatus = None,
            action_datetime: dt.datetime = None,
            rating_score: int = 0,
            is_favourite: bool = False
    ) -> None:
        """
        This is the Movie class constructor
        """
        if not isinstance(movie_info, MovieInfo):
            raise TypeError("'movie_info' must be a 'MovieInfo' object")
        if watch_status is not None and \
           not isinstance(watch_status, WatchStatus):
            raise TypeError("'watch_status' must be a 'WatchStatus' enum")
        if action_datetime is not None and \
           not isinstance(action_datetime, dt.datetime):
            raise TypeError(
                "'action_datetime' must be a 'datetime.datetime' object"
            )
        if not isinstance(rating_score, int):
            raise TypeError("'rating_score' must be an integer")
        if not isinstance(is_favourite, bool):
            raise TypeError("'is_favourite' must be a boolean")

        self.movie_info = movie_info
        self.watch_status = watch_status
        self.action_datetime = action_datetime
        self.rating_score = rating_score
        self.is_favourite = is_favourite

    def __str__(self) -> str:
        return str(self.movie_info)

    def load_movie_details(self) -> None:
        """
        Load movie details
        """
        self.movie_info.fetch()
        self.load_watch_status()
        self.load_favourite_status()

    def load_watch_status(self) -> None:
        """
        Load watch status
        """
        self.watch_status = WatchStatus.DEFAULT

        watchlist = \
            helpers.parse_data(
                helpers.read_list_from_file(helpers.FileType.WATCHLIST)
            )
        for movie_id, action_datetime in watchlist:
            if self.movie_info.movie_id == int(movie_id):
                self.watch_status = WatchStatus.WATCHLIST
                self.action_datetime = \
                    helpers.string_to_datetime(action_datetime)

        watched_list = \
            helpers.parse_data(
                helpers.read_list_from_file(helpers.FileType.WATCHED)
            )
        for movie_id, rating_score, action_datetime in watched_list:
            if self.movie_info.movie_id == int(movie_id):
                if rating_score == "0":
                    self.watch_status = WatchStatus.WATCHED
                else:
                    self.watch_status = WatchStatus.RATED
                self.action_datetime = \
                    helpers.string_to_datetime(action_datetime)
                self.rating_score = int(rating_score)

    def set_rating_score(self, score: int) -> None:
        """
        Rate the movie and save it to your watched list (watched).
        """
        if not isinstance(score, int):
            raise TypeError("'score' must be an integer")
        if score < 0 or score > 10:
            raise ValueError("'score' must be between 1 and 10")

        self.rating_score = score

        watched_lines = helpers.read_list_from_file(helpers.FileType.WATCHED)
        new_watched_lines = []
        for line in watched_lines:
            if not line.startswith(f"{self.movie_info.movie_id}|"):
                new_watched_lines.append(line)
        new_watched_lines.append(
            f"{self.movie_info.movie_id}|"
            f"{self.rating_score}|"
            f"{dt.datetime.now()}\n"
        )

        helpers.save_list_to_file(helpers.FileType.WATCHED, new_watched_lines)

    def remove_rating_score(self) -> None:
        """
        Remove rating score
        """
        self.set_rating_score(0)

    def load_favourite_status(self) -> None:
        """
        Load favourite status
        """
        self.is_favourite = self.get_favourite_status()

    def get_favourite_status(self) -> bool:
        """
        Get favourite status
        """
        favourites = \
            helpers.parse_data(
                helpers.read_list_from_file(helpers.FileType.FAVOURITES)
            )
        for favourite in favourites:
            if self.movie_info.movie_id == int(favourite[0]):
                return True
        return False

    def set_favourite_status(self, is_favourite: bool) -> None:
        """
        Set favourite status
        """
        if is_favourite:
            self.add_to_favourites()
        else:
            self.remove_from_favourites()

    def add_to_favourites(self) -> None:
        """
        Add to favourite list (favourites).
        """
        data = f"{self.movie_info.movie_id}|{dt.datetime.now()}\n"
        helpers.append_data_to_file(helpers.FileType.FAVOURITES, data)

    def remove_from_favourites(self) -> None:
        """
        Remove frome favourite list (favourites).
        """
        self.remove_movie_from_list(helpers.FileType.FAVOURITES)

    def add_to_watched_list(self) -> None:
        """
        Add to watched list (watched).
        """
        data = \
            f"{self.movie_info.movie_id}|"\
            f"{self.rating_score}|"\
            f"{dt.datetime.now()}\n"
        helpers.append_data_to_file(helpers.FileType.WATCHED, data)

    def remove_from_watched_list(self) -> None:
        """
        Remove from watched list (watched).
        """
        self.remove_movie_from_list(helpers.FileType.WATCHED)

    def add_to_watchlist(self) -> None:
        """
        Add to want to watch list (watchlist).
        """
        data = f"{self.movie_info.movie_id}|{dt.datetime.now()}\n"
        helpers.append_data_to_file(helpers.FileType.WATCHLIST, data)

    def remove_from_watchlist(self) -> None:
        """
        Remove from want to watch list (watchlist).
        """
        self.remove_movie_from_list(helpers.FileType.WATCHLIST)

    def remove_movie_from_list(self, file_type: helpers.FileType) -> None:
        """
        Remove movie from file depending on the FileType.
        """
        lines = helpers.read_list_from_file(file_type)
        new_lines = []
        for line in lines:
            if not line.startswith(f"{self.movie_info.movie_id}|"):
                new_lines.append(line)

        helpers.save_list_to_file(file_type, new_lines)
