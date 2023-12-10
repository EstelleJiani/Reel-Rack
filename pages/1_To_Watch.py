"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the want to watch list (watchlist) page.
"""

import streamlit as st

import page_helpers as ph
from models.movie_list import MovieList

MESSAGE = \
    "Your current watch list is empty. Go to the homepage to check out "\
    "the latest trending movies and add the movies you want to "\
    "watch to watch list!"


# If the 'page' variable does not exist in the Session State
# we create the 'page' variable and assign it the value 'original'
if "page" not in st.session_state:
    st.session_state["page"] = "original"

# Check if the value of 'page' is 'watchlist_movie',
# then run the code from 'page_helpers' to display movie details.
if st.session_state["page"] == "watchlist_movie":
    ph.show_movie_details(st.session_state["movie_id"])
# Otherwise (e.g. when the value of 'page' is 'original' or other value),
# display the content of the to watch list itself.
else:
    # Set the page title, icon and the layout.
    ph.set_page_config("To Watch List")

    # Get the watchlist from the watchlist file.
    watchlist = MovieList()
    watchlist.load_watchlist()

    if len(watchlist) > 0:
        # Show the watchlist page.
        ph.show_movie_list(watchlist, "watchlist_movie")
    else:
        ph.show_empty_list_message(MESSAGE)
