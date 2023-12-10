"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

This is the favourite list (favourites) page.
"""
import streamlit as st

import page_helpers as ph
from models.movie_list import MovieList

MESSAGE = \
    "Your current favourites is empty. Explore the homepage to find and "\
    "add your favourite movies to the list!"


# If the 'page' variable does not exist in the Session State
# we create the 'page' variable and assign it the value 'original'
if "page" not in st.session_state:
    st.session_state["page"] = "original"

# Check if the value of 'page' is 'favourite_movie',
# then run the code from 'page_helpers' to display movie details.
if st.session_state["page"] == "favourite_movie":
    ph.show_movie_details(st.session_state["movie_id"])
# Otherwise (e.g. when the value of 'page' is 'original' or other value),
# display the content of the favourites itself.
else:
    # Set the page title, icon and the layout.
    ph.set_page_config("Favourites")

    # Get the favourite list from the favourites file.
    favourites = MovieList()
    favourites.load_favourites()

    if len(favourites) > 0:
        # Show the favourite page.
        ph.show_movie_list(favourites, "favourite_movie")
    else:
        ph.show_empty_list_message(MESSAGE)
