"""
CS5001 Final Project
ReelRack
Jiani Guo Dec 2023

The general API information.
"""

# HEADERS includes the Bearer Token, SECRET and IMPORTANT!
HEADERS = {
    "accept": "application/json",
    "Authorization":
        # ADD YOU Access Token Auth HERE
        ""
}

# Query the API configuration details.
CONFIGURATION_DETAILS_URL = "https://api.themoviedb.org/3/configuration"
# Get the trending movies on TMDB.
# time_window: day, week
TRENDING_MOVIES = "https://api.themoviedb.org/3/trending/movie/"
# Search for movies by their original, translated and alternative titles.
SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
# Get the top level details of a movie by ID.
MOVIES_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
