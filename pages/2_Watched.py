"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the watched list (watched) page.
"""

import streamlit as st

import page_helpers as ph
from models.movie_list import MovieList

MESSAGE = \
    "Your current watched list is empty. Head to the homepage to search for "\
    "movies you've seen before and add them to your watched list!"


# If the 'page' variable does not exist in the Session State
# we create the 'page' variable and assign it the value 'original'
if "page" not in st.session_state:
    st.session_state["page"] = "original"

# Check if the value of 'page' is 'watched_movie',
# then run the code from 'page_helpers' to display movie details.
if st.session_state["page"] == "watched_movie":
    ph.show_movie_details(st.session_state["movie_id"])
# Otherwise (e.g. when the value of 'page' is 'original' or other value),
# display the content of the watched list itself.
else:
    # Set the page title, icon and the layout.
    ph.set_page_config("Watched List")

    # Get the watched list from the watched file.
    watched_list = MovieList()
    watched_list.load_watched_list()

    if len(watched_list) > 0:
        # Show the watchlist page.
        ph.show_movie_list(watched_list, "watched_movie")
    else:
        ph.show_empty_list_message(MESSAGE)
