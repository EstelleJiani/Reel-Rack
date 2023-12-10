"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the homepage (entrypoint file)
"""
import streamlit as st

import page_helpers as ph
from models.movie_list import MovieList

# As the API returns 20 trending movies at a time, I have set the layout
# to display 5 movies per row.
# Thus, we only need 4 rows and 5 columns to show these trending movies.
MOVIES_PER_ROW = 5

ERROR_MESSAGE = "Oops! Something went wrong. Please try again later."


def nav_to_movie_details_page(movie_id: int) -> None:
    """
    Show the movie details.
    """
    st.session_state["movie_id"] = movie_id
    st.session_state["page"] = "home_movie"


def show_trending_movie_list(
        trending_movie_list: MovieList,
        time_window: str
) -> None:
    """
    Show trending movie list
    """
    rows = len(trending_movie_list) // MOVIES_PER_ROW
    columns = MOVIES_PER_ROW

    for i in range(rows):
        cols = st.columns(columns)

        for j in range(columns):
            movie_index = i * columns + j

            if movie_index < len(trending_movie_list):
                with cols[j]:
                    trending_movie = trending_movie_list[movie_index]
                    st.image(
                        trending_movie.movie_info.poster_url,
                        trending_movie.movie_info.title,
                        use_column_width=True
                    )
                    st.button(
                        "More",
                        key=f"movie_{trending_movie.movie_info.movie_id}_"
                            f"{time_window}",
                        on_click=nav_to_movie_details_page,
                        args=[trending_movie.movie_info.movie_id],
                        use_container_width=True
                    )
        st.divider()


def show_movies_from_search(search_results_list: MovieList) -> None:
    """
    Show movies from search
    """
    for movie in search_results_list.movies:
        col1, col2 = st.columns([1, 3])
        col1.image(movie.movie_info.poster_url)
        with col2:
            st.header(movie)
            st.write(movie.movie_info.overview)
            st.button(
                "More",
                movie.movie_info.movie_id,
                on_click=nav_to_movie_details_page,
                args=[movie.movie_info.movie_id]
            )

        st.divider()


def show_no_results_found(search_keyword: str) -> None:
    """
    Show no resultes found
    """
    col = st.columns((1, 4, 1))
    with col[1]:
        st.subheader(
            "There are no movies that matched your "
            f"search for '{search_keyword}'. "
            "Please try a different keyword or "
            "check the spelling and try again."
        )


# If the 'page' variable does not exist in the Session State
# we create the 'page' variable and assign it the value 'original'
if "page" not in st.session_state:
    st.session_state["page"] = "original"

# Check if the value of 'page' is 'home_movie',
# then run the code from 'page_helpers' to display movie details.
if st.session_state["page"] == "home_movie":
    ph.show_movie_details(st.session_state["movie_id"])

# Otherwise (e.g. when the value of 'page' is 'original' or other value),
# display the content of the Homepage itself.
else:
    # Set the page title, icon and the layout.
    ph.set_page_config()

    st.title("🎞 Reel Rack")
    query = st.text_input("search for a movie")

    movie_list = MovieList()
    # If there is a content in text input (search bar),
    # then show the searching result.
    if query != '':
        with st.spinner('Searching...'):
            movie_list.fetch_movies_from_search(query)
        if len(movie_list) > 0:
            show_movies_from_search(movie_list)
        else:
            show_no_results_found(query)
    # If there is no content in text input (search bar),
    # then show the trending movies by day.
    else:
        st.header("Trending")
        day, week = st.tabs(("Day", "Week"))
        with day:
            with st.spinner('Loading...'):
                movie_list.fetch_trending_movies("day")
            if len(movie_list) > 0:
                show_trending_movie_list(movie_list, "day")
            else:
                st.error(ERROR_MESSAGE)

        with week:
            with st.spinner('Loading...'):
                movie_list.fetch_trending_movies("week")
            if len(movie_list) > 0:
                show_trending_movie_list(movie_list, "week")
            else:
                st.error(ERROR_MESSAGE)


# below code were used to debug, show the session state object.
# st.write("st.session_state object:", st.session_state)
