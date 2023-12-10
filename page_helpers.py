"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This the helpers for pages.
"""

import streamlit as st

from models.movie import Movie, WatchStatus
from models.movie_info import MovieInfo

WEBSITE_NAME = "Reel Rack"

FAVICON = "🎞"
FAVOURITE_ICON = "❤️"
UNFAVOURITE_ICON = "💔"
UNRATE_ICON = "☆"

MIN_SCORE = 1
MAX_SCORE = 10
DEFAULT_SCORE = 5


def add_to_favourites(movie: Movie) -> None:
    """
    Add to favourite list (favourites).
    """
    movie.add_to_favourites()
    st.toast("Added", icon=FAVOURITE_ICON)


def remove_from_favourites(movie: Movie) -> None:
    """
    Remove from favourite list (favourites).
    """
    movie.remove_from_favourites()
    st.toast("Removed", icon=UNFAVOURITE_ICON)


def add_to_watched_list(movie: Movie) -> None:
    """
    Add to watched list (watched).
    """
    movie.remove_from_watchlist()
    movie.add_to_watched_list()
    st.balloons()


def remove_from_watched_list(movie: Movie) -> None:
    """
    Remove from watched list (watched).
    """
    movie.remove_from_watched_list()
    st.balloons()


def add_to_watchlist(movie: Movie) -> None:
    """
    Add to want to watch list (watchlist).
    """
    movie.add_to_watchlist()
    st.balloons()


def remove_from_watchlist(movie: Movie) -> None:
    """
    Remove from want to watch list (watchlist).
    """
    movie.remove_from_watchlist()
    st.balloons()


def set_rating_score(movie: Movie, score) -> None:
    """
    Rate the movie and save it to your watched list (watched).
    """
    movie.set_rating_score(score)
    st.balloons()


def remove_rating_score(movie: Movie) -> None:
    """
    Remove rating score
    """
    movie.remove_rating_score()
    st.balloons()


def back_to_original() -> None:
    """
    Set the page value to navigate back to original page
    """
    st.session_state["page"] = "original"


def nav_to_movie_details_page(movie_id: int, page: str) -> None:
    """
    Show the movie details.
    """
    st.session_state["movie_id"] = movie_id
    st.session_state["page"] = page


def set_page_config(info: str = None) -> None:
    """
    Set page config
    Set the page title, icon and the layout.
    """
    page_title = WEBSITE_NAME
    if info is not None:
        page_title = f"{info} - {WEBSITE_NAME}"

    st.set_page_config(
        page_title=page_title,
        page_icon=FAVICON,
        layout="wide"
    )


def show_rating_form(movie: Movie) -> None:
    """
    Show rating form
    """
    rating_form = st.empty()

    with rating_form.form("Rating form"):
        score = st.slider(
            "Rate this movie",
            MIN_SCORE,
            MAX_SCORE,
            DEFAULT_SCORE
        )
        rating_submit_button = st.form_submit_button("Submit")

        if rating_submit_button:
            set_rating_score(movie, score)
            rating_form.empty()
            st.rerun()


def show_movie_action_buttons(movie: Movie) -> None:
    """
    Show movie action buttons
    """
    subcol = st.columns([0.15, 0.25, 0.25, 0.35])

    if not movie.is_favourite:
        # favourite button
        subcol[0].button(
            FAVOURITE_ICON,
            help="Add to favourites",
            on_click=add_to_favourites,
            args=[movie]
        )
    else:
        # unfavourite_button
        subcol[0].button(
            UNFAVOURITE_ICON,
            help="Remove frome favourites",
            on_click=remove_from_favourites,
            args=[movie]
        )

    if movie.watch_status == WatchStatus.DEFAULT:
        # watchlist button
        subcol[1].button(
            "Add to watchlist",
            on_click=add_to_watchlist,
            args=[movie],
            type="primary",
            use_container_width=True
        )
        # watched button
        subcol[2].button(
            "Add to watched",
            on_click=add_to_watched_list,
            args=[movie],
            type="primary",
            use_container_width=True
        )
    elif movie.watch_status == WatchStatus.WATCHLIST:
        # watchlist remove button
        subcol[1].button(
            "Remove from watchlist",
            on_click=remove_from_watchlist,
            args=[movie],
            use_container_width=True
        )
        # watched button
        subcol[2].button(
            "Add to watched",
            on_click=add_to_watched_list,
            args=[movie],
            type="primary",
            use_container_width=True
        )
    elif movie.watch_status == WatchStatus.WATCHED:
        # watched remove button
        subcol[1].button(
            "Remove from Watched",
            on_click=remove_from_watched_list,
            args=[movie],
            use_container_width=True
        )

        show_rating_form(movie)
    elif movie.watch_status == WatchStatus.RATED:
        # unrate_button
        subcol[1].button(
            UNRATE_ICON,
            help="Clear my rating",
            on_click=remove_rating_score,
            args=[movie]
        )
        subcol[2].write(f"{movie.rating_score} / {MAX_SCORE}")


def show_movie_details(movie_id: int) -> None:
    """
    Show the movie details by movie_id.
    """
    movie = Movie(MovieInfo(movie_id))
    movie.load_movie_details()

    # Set the page title, icon and the layout.
    set_page_config(str(movie))

    # Layout for the movie details page.
    st.button(
        'Back',
        on_click=back_to_original
    )

    col1, col2 = st.columns([1, 3])
    col1.image(movie.movie_info.poster_url)
    with col2:
        st.title(movie)
        st.markdown(f"*Release Date:* {movie.movie_info.release_date}")
        st.markdown(
            "##### Overview:  \n"
            f"{movie.movie_info.overview}"
        )

        show_movie_action_buttons(movie)


def show_movie_list(movie_list: list, page: str) -> None:
    """
    Show movie list
    """
    for movie in movie_list:
        movie = Movie(MovieInfo(int(movie.movie_info.movie_id)))
        with st.spinner('Loading...'):
            movie.load_movie_details()
        col1, col2 = st.columns([1, 3])
        col1.image(movie.movie_info.poster_url)
        with col2:
            st.title(movie)
            st.write(movie.movie_info.overview)
            st.button(
                "More",
                movie.movie_info.movie_id,
                on_click=nav_to_movie_details_page,
                args=(movie.movie_info.movie_id, page)
            )
            if page == "watchlist_movie" or page == "watched_movie":
                st.caption(
                    "Add on: "
                    f"{movie.action_datetime.strftime('%Y-%m-%d')}",
                    help=movie.action_datetime.strftime('%Y-%m-%d %H:%M:%S')
                )
        st.divider()


def show_empty_list_message(message: str) -> None:
    """
    Show an empty list, and guide user to add movie to list.
    """
    st.title("🎞 Reel Rack")
    col = st.columns((1, 4, 1))
    with col[1]:
        st.subheader(message)
        st.link_button("Back to Home", "Home")
